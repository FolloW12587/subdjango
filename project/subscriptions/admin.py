from django.contrib import admin


from . import models, filters


class SubscriptionModelAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "wb_product_limit", "ozon_product_limit", "price_rub")
    search_fields = (
        "id",
        "name",
    )


admin.site.register(models.Subscription, SubscriptionModelAdmin)


class UserSubscriptionModelAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "subscription", "active_from", "active_to")
    search_fields = ("id", "user__username", "user__tg_id")

    list_select_related = ("user", "subscription")
    list_filter = ("subscription", filters.UserSubscriptionStatusFilter)


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
