from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers

from .models import Account, Transaction, TransactionTypes
from .services import create_account, create_transaction, get_transactions, get_all_accounts, get_account_by_uid


class AccountView(APIView):

    class AccountCreateSerializer(serializers.ModelSerializer):
        class Meta:
            model = Account
            fields = ['currency']

    class AccountGetSerializer(serializers.ModelSerializer):
        class Meta:
            model = Account
            fields = ['uid', 'currency', 'balance']

    def post(self, request):
        """Создание нового банковского счета."""
        serializer = self.AccountCreateSerializer(data=request.data)
        if serializer.is_valid():
            account = create_account(
                currency=serializer.validated_data['currency']
            )
            return Response(self.AccountGetSerializer(account).data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        """Получение списка всех счетов."""
        accounts = get_all_accounts()
        serializer = self.AccountGetSerializer(accounts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TransactionView(APIView):

    class TransactionGetSerializer(serializers.ModelSerializer):
        class Meta:
            model = Transaction
            fields = ['transaction_type', 'amount', 'created_at']

    class TransactionCreateSerializer(serializers.ModelSerializer):
        transaction_type = serializers.ChoiceField(choices=TransactionTypes)
        amount = serializers.IntegerField()

        class Meta:
            model = Transaction
            fields = ['transaction_type', 'amount']

        def validate_amount(self, value):
            if value <= 0:
                raise serializers.ValidationError("Сумма должна быть положительной.")
            return value

    def post(self, request, account_uid):
        """Создание транзакции для существующего счета."""
        serializer = self.TransactionCreateSerializer(data=request.data)

        if serializer.is_valid():
            account = get_object_or_404(Account, uid=account_uid)

            try:
                transaction = create_transaction(
                    account=account,
                    transaction_type=serializer.validated_data['transaction_type'],
                    amount=serializer.validated_data['amount']
                )
            except ValidationError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

            return Response(self.TransactionGetSerializer(transaction).data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, account_uid):
        """Получение списка всех транзакций для конкретного счета."""
        try:
            account = get_account_by_uid(account_uid)
            transactions = get_transactions(account)
            serializer = self.TransactionGetSerializer(transactions, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
