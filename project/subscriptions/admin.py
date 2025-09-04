from django.contrib import admin
from django.db.models import Count, OuterRef, Subquery

from main.models import UserProducts
from . import models, filters


class SubscriptionModelAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "wb_product_limit", "ozon_product_limit", "price_rub")
    search_fields = (
        "id",
        "name",
    )


admin.site.register(models.Subscription, SubscriptionModelAdmin)


class UserSubscriptionModelAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "subscription",
        "active_from",
        "active_to",
        "product_count",
    )
    search_fields = ("id", "user__username", "user__tg_id")

    list_select_related = ("user", "subscription")
    list_filter = ("subscription", filters.UserSubscriptionStatusFilter)

    def product_count(self, obj):
        return obj.product_count or 0

    product_count.short_description = "Число продуктов"
    product_count.admin_order_field = "product_count"

    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        subquery = (
            UserProducts.objects.filter(user_id=OuterRef("user_id"))
            .values("user_id")
            .annotate(total=Count("id"))
            .values("total")
        )

        return queryset.annotate(product_count=Subquery(subquery))


admin.site.register(models.UserSubscription, UserSubscriptionModelAdmin)


class OrderModelAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "subscription", "status", "created_at")
    search_fields = ("id", "user__username", "user__tg_id")

    list_select_related = ("user", "subscription")
    list_filter = ("subscription", "status")


admin.site.register(models.Order, OrderModelAdmin)


class TransactionModelAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "provider", "amount", "transaction_datetime")
    search_fields = (
        "id",
        "user__username",
        "user__tg_id",
        "order__id",
        "provider_txn_id",
    )

    list_select_related = ("user", "order")

    list_filter = ("provider",)


admin.site.register(models.Transaction, TransactionModelAdmin)
