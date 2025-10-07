from uuid import uuid4
from django.db import models

from main.models import Users


class Subscription(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField("Название", max_length=255)
    wb_product_limit = models.IntegerField("Лимит на продукты вб")
    ozon_product_limit = models.IntegerField("Лимит на продукты озона")
    price_rub = models.IntegerField("Цена подписки в рублях")

    class Meta:
        managed = False
        db_table = "subscriptions"
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"

    def __str__(self):
        return f"<Подписка {self.name} (wb: {self.wb_product_limit}, ozon: {self.ozon_product_limit}) за {self.price_rub}"


class UserSubscription(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(
        Users, verbose_name="Пользователь", on_delete=models.CASCADE
    )
    order = models.ForeignKey("Order", verbose_name="Платеж", on_delete=models.CASCADE)
    subscription = models.ForeignKey(
        Subscription, verbose_name="Подписка", on_delete=models.CASCADE
    )
    active_from = models.DateField("Активна с")
    active_to = models.DateField("Активна по", null=True, blank=True, default=None)

    class Meta:
        managed = False
        db_table = "user_subscriptions"
        verbose_name = "Подписка пользователя"
        verbose_name_plural = "Подписки пользователей"


class Transaction(models.Model):
    PAYMENT_PROVIDERS = (("YOOMONEY", "Юмани"),)

    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(
        Users, verbose_name="Пользователь", on_delete=models.CASCADE
    )
    order = models.ForeignKey("Order", verbose_name="Платеж", on_delete=models.CASCADE)

    provider = models.CharField("Провайдер", choices=PAYMENT_PROVIDERS, max_length=63)
    provider_txn_id = models.CharField(
        "Идентификатор в платежной систерме", max_length=255
    )

    amount = models.FloatField("Количество")
    currency = models.CharField("Валюта", max_length=255)

    transaction_datetime = models.DateTimeField("Время транзакции")

    raw_data = models.TextField("Сырые данные с платежки")
    created_at = models.DateTimeField("Создана в", auto_now_add=True)

    class Meta:
        managed = False
        db_table = "transactions"
        verbose_name = "Транзакция"
        verbose_name_plural = "Транзакции"

    def __str__(self):
        return f"<Transaction {self.provider} {self.amount}>"


class Order(models.Model):
    ORDER_STATUSES = (
        ("PENDING", "Предстоящая"),
        ("SUCCESS", "Успешная"),
        ("FAILED", "Неуспешная"),
    )

    id = models.UUIDField(primary_key=True, default=uuid4)
    user = models.ForeignKey(
        Users, verbose_name="Пользователь", on_delete=models.CASCADE
    )
    subscription = models.ForeignKey(
        Subscription, verbose_name="Подписка", on_delete=models.CASCADE
    )
    status = models.CharField("Статус", choices=ORDER_STATUSES, max_length=255)
    price = models.FloatField("Сумма платежа")

    created_at = models.DateTimeField("Создана в", auto_now_add=True)

    class Meta:
        managed = False
        db_table = "orders"
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
