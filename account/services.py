from django.db import transaction as db_transaction
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError

from account.models import Account, TransactionTypes, Transaction


def create_account(currency):
    """Создание нового банковского счета."""
    return Account.objects.create(currency=currency)


def get_account_by_uid(account_uid):
    """Получение аккаунта по UID."""
    return get_object_or_404(Account, uid=account_uid)


def get_all_accounts():
    """Получение списка всех аккаунтов."""
    return Account.objects.all()


def create_transaction(account, transaction_type, amount):
    """Создание транзакции."""
    if amount <= 0:
        raise ValidationError("Сумма должна быть положительной.")

    with db_transaction.atomic():
        if transaction_type == TransactionTypes.WITHDRAWAL and account.balance < amount:
            raise ValidationError("Недостаточно средств.")

        transaction = Transaction.objects.create(
            account=account,
            transaction_type=transaction_type.value,
            amount=amount
        )

        if transaction_type == TransactionTypes.DEPOSIT:
            account.balance += amount
        else:
            account.balance -= amount
        account.save()

    return transaction


def get_transactions(account):
    """Получение всех транзакций для конкретного счета."""
    return account.transactions.all()
