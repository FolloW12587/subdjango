from django.contrib import admin

from main.models import Products

from .models import CategoryChannelLink, Category, ChannelLink, PopularProduct
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
    )

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
