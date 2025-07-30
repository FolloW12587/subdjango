from django.contrib import admin

from . import models


class MessageSendingButtonInline(admin.TabularInline):
    model = models.MessageSendingButton


class MessageSendingModelAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "status",
        "started_at",
        "ended_at",
        "users_to_notify",
        "users_notified",
    )

    list_filter = ("status",)
    inlines = (MessageSendingButtonInline,)
    actions = ("test_sending", "mark_as_upcoming")

    @admin.action(description="Протестировать")
    def test_sending(self, request, queryset):
        queryset.update(status="TEST")

    @admin.action(description="Добавить в очередь")
    def mark_as_upcoming(self, request, queryset):
        queryset.update(status="UPCOMING")


admin.site.register(models.MessageSending, MessageSendingModelAdmin)


class MessageSendingButtonModelAdmin(admin.ModelAdmin):
    list_display = ("id", "message_sending", "type", "text", "data")
    list_select_related = ("message_sending",)

    list_filter = ("message_sending__status", "message_sending")


admin.site.register(models.MessageSendingButton, MessageSendingButtonModelAdmin)
