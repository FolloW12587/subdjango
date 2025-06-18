from django.contrib import admin, messages
from django.shortcuts import redirect
from django.utils.html import format_html
from django.urls import path

from main.models import Products

from .models import (
    CategoryChannelLink,
    Category,
    ChannelLink,
    PopularProduct,
    PopularProductSaleRange,
)
from popular_products.filters import CustomCategoryFilter

# Register your models here.


class CategoryChannelLinkInline(admin.TabularInline):
    model = CategoryChannelLink
    extra = 1


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    inlines = [
        CategoryChannelLinkInline,
    ]


admin.site.register(Category, CategoryAdmin)


class ChannelLinkAdmin(admin.ModelAdmin):
    list_display = ("name",)


admin.site.register(ChannelLink, ChannelLinkAdmin)


class PopularProductAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "category",
        "clickable_link",
    )

    def clickable_link(self, instance: PopularProduct):
        return format_html(
            '<a href="{0}" target="_blank">Перейти</a>',
            instance.link,
        )

    clickable_link.short_description = "Link"

    raw_id_fields = (
        "category",
        "product",
    )

    list_filter = (CustomCategoryFilter,)

    search_fields = ("id", "product__name")

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related("product", "category", "category__parent")
        )


admin.site.register(PopularProduct, PopularProductAdmin)


class ProductsAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "product_marker",
    )
    search_fields = ("id", "name")


admin.site.register(Products, ProductsAdmin)


class PopularProductSaleRangeAdmin(admin.ModelAdmin):
    list_display = ("start_price", "end_price", "coefficient")

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "update_discounts/",
                self.admin_site.admin_view(self.update_discounts),
                name="update_popular_product_discounts",
            ),
        ]
        return custom_urls + urls

    def changelist_view(self, request, extra_context=None):
        if extra_context is None:
            extra_context = {}
        extra_context["custom_button"] = True
        return super().changelist_view(request, extra_context=extra_context)

    def update_discounts(self, request):
        ranges = list(PopularProductSaleRange.objects.all().order_by("start_price"))
        updated_count = 0

        for product in PopularProduct.objects.all():
            for r in ranges:
                if r.start_price <= product.start_price < r.end_price:
                    product.sale = int(product.start_price * r.coefficient)
                    product.save(update_fields=["sale"])
                    updated_count += 1
                    break

        self.message_user(request, f"Обновлено {updated_count} популярных товаров.", level=messages.SUCCESS)
        return redirect("..")


admin.site.register(PopularProductSaleRange, PopularProductSaleRangeAdmin)
