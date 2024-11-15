import uuid

from django.db import models
from enum import Enum


class Currencies(Enum):
    USD = 'USD'
    RUB = 'RUB'
    EUR = 'EUR'


class TransactionTypes(Enum):
    DEPOSIT = 'deposit'
    WITHDRAWAL = 'withdrawal'


class Account(models.Model):
    uid = models.UUIDField(
        'Уникальный uid',
        default=uuid.uuid4,
        unique=True
    )
    currency = models.CharField(
        'ISO код валюты',
        max_length=3,
        choices=[(currency.value, currency.value) for currency in Currencies],
        null=False,
        blank=False
    )
    balance = models.BigIntegerField(
        'Баланс в копейках или центах',
        default=0
    )


class Transaction(models.Model):
    account = models.ForeignKey(
        related_name='transactions',
        to=Account,
        on_delete=models.CASCADE,
    )
    transaction_type = models.CharField(
        'Тип транзакции',
        max_length=30,
        choices=[(t_type.value, t_type.value) for t_type in TransactionTypes],
    )
    amount = models.BigIntegerField(
        'Сумма в копейках или центах',
        null=False,
    )
    created_at = models.DateTimeField(
        'Дата создания',
        auto_now_add=True,
    )
