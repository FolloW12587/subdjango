from django.utils import timezone
from django.contrib import admin


class UserSubscriptionStatusFilter(admin.SimpleListFilter):
    title = "Статус"
    parameter_name = "status"

    USED = "used"
    ACTIVE = "active"
    UPCOMING = "upcoming"

    def lookups(self, request, model_admin):
        # Используйте select_related для оптимизации запроса
        return (
            (self.USED, "Использована"),
            (self.ACTIVE, "Активна"),
            (self.UPCOMING, "В ожидании начала"),
        )

    def queryset(self, request, queryset):
        now = timezone.now().date()
        match self.value():
            case self.USED:
                return queryset.filter(active_to__lt=now)
            case self.ACTIVE:
                return queryset.filter(active_from__gte=now, active_to__lte=now)
            case self.UPCOMING:
                return queryset.filter(active_from__gt=now)
            case _:
                return queryset
