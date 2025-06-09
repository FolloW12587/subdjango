from django.contrib import admin

from .models import Category


class CustomCategoryFilter(admin.SimpleListFilter):
    title = "Direction"
    parameter_name = "direction"

    def lookups(self, request, model_admin):
        # Используйте select_related для оптимизации запроса
        directions = Category.objects.select_related("parent").distinct()
        return [(d.id, str(d)) for d in directions]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(category__id=self.value())
        return queryset
