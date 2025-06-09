from django.contrib import admin
from django.db.models import Count, Value, OuterRef, Subquery, F
from django.db.models.functions import Coalesce
from django.urls import path


from .models import Users, UTM, UserProducts
from .views import custom_admin_view
from .filters import CustomDateTimeFilter

from rangefilter.filters import DateRangeFilterBuilder


class MyAdminSite(admin.AdminSite):
    # index_template = "admin/custom_index.html"
    # site_header = "Custom Administration"
    def dashboard_page(self, request):
        return custom_admin_view(request, self=self)
        # context = {"text": "Hello Admin",
        #            "page_name": "Custom Page"}
        # return TemplateResponse(request,
        #                         "admin/custom_page.html",
        #                         context)

    def get_urls(self):
        urls = super().get_urls()
        # print(urls)
        custom_urls = [
            path(
                "dashboard/",
                admin.site.admin_view(self.dashboard_page),
                name="dashboard_page",
            ),
        ]
        return custom_urls + urls

    def get_app_list(self, request, app_label=None):
        app_list = super().get_app_list(request, app_label)
        if app_label is None or app_label == "custom":
            app_list.append(
                {
                    "name": "Общее",
                    "app_label": "custom",
                    "models": [
                        {
                            "name": "Статистика бота",
                            "object_name": "dashboard",
                            "admin_url": "/admin/dashboard",
                            "view_only": True,
                        }
                    ],
                }
            )
        return app_list


admin.site = MyAdminSite()

# admin.site.unregister(User)
# admin.site.unregister(Group)


class UTMInline(admin.StackedInline):
    model = UTM
    extra = 0
    classes = [
        "collapse",
    ]

    def has_change_permission(self, request, obj=...):
        return False


# Отображение комментариев в админ панели
# @admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        # 'tg_id',
        # 'link_count',
        # 'is_active',
        "get_utm_source",
        "utm__utm_campaign",
        "product_count",
        "product_all_time_count",
        "time_create",
    )
    inlines = [UTMInline]

    def get_utm_source(self, obj):
        return (
            obj.utm_source
            if obj.utm_source and (obj.utm_source.find("_") != 1)
            else obj.utm.source
        )

    get_utm_source.short_description = "UTM источник"

    readonly_fields = (
        # 'link_count',
        "username",
        "first_name",
        "last_name",
        "utm_source",
        "time_create",
        # 'subscription',
        "product_count",
        "product_all_time_count",
    )

    ordering = ("-time_create",)

    list_filter = (
        CustomDateTimeFilter,
        ("time_create", DateRangeFilterBuilder()),
        # UTMSourceFilter,
        # ('time_create', DateRangeQuickSelectListFilterBuilder()),
        # ("time_create", NumericRangeFilterBuilder()),
        # 'time_create',
        # UTMSourceSecondPartFilter,
    )

    fieldsets = [
        (
            None,
            {
                "fields": [
                    "username",
                    "first_name",
                    "last_name",
                    "subscription",
                    "utm_source",
                    "product_count",
                    "product_all_time_count",
                    #    'related_utm',
                    "time_create",
                ]
            },
        ),
    ]

    def product_count(self, obj):
        wb_products = obj.wb_product_count if obj.wb_product_count else 0
        ozon_products = obj.ozon_product_count if obj.ozon_product_count else 0

        product_count = wb_products + ozon_products

        return f"{product_count} | wb: {wb_products} | ozon: {ozon_products}"

    def product_all_time_count(self, obj):
        wb_products = obj.wb_total_count
        ozon_products = obj.ozon_total_count

        product_count = wb_products + ozon_products

        return f"{product_count} | wb: {wb_products} | ozon: {ozon_products}"

    product_count.short_description = "Число продуктов"
    product_count.admin_order_field = "all_product_count"

    product_all_time_count.short_description = "Число продуктов за всё время"
    product_all_time_count.admin_order_field = "all_product_count"

    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        # wb_products_subquery = WbProducts.objects.filter(
        #     user_id=OuterRef('tg_id')
        # ).values('user_id').annotate(
        #     total_count=Coalesce(Count('id'), Value(0))
        # ).values('total_count')

        wb_products_subquery = (
            UserProducts.objects.select_related("product")
            .filter(
                user_id=OuterRef("tg_id"),
                product__product_marker="wb",
            )
            .values("user_id")
            .annotate(total_count=Coalesce(Count("id"), Value(0)))
            .values("total_count")
        )

        # ozon_products_subquery = OzonProducts.objects.filter(
        #     user_id=OuterRef('tg_id')
        # ).values('user_id').annotate(
        #     total_count=Coalesce(Count('id'), Value(0))
        # ).values('total_count')

        ozon_products_subquery = (
            UserProducts.objects.select_related("product")
            .filter(
                user_id=OuterRef("tg_id"),
                product__product_marker="ozon",
            )
            .values("user_id")
            .annotate(total_count=Coalesce(Count("id"), Value(0)))
            .values("total_count")
        )

        return queryset.select_related("utm").annotate(
            wb_product_count=Subquery(wb_products_subquery),
            ozon_product_count=Subquery(ozon_products_subquery),
            all_product_count=Coalesce(F("wb_product_count"), Value(0))
            + Coalesce(F("ozon_product_count"), Value(0)),
            all_product_all_time_count=Coalesce(F("wb_total_count"), Value(0))
            + Coalesce(F("ozon_total_count"), Value(0)),
        )


admin.site.register(Users, UsersAdmin)


class UserProductsAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "product_name",
        "product_marker",
        "time_create",
    )

    list_filter = (
        # 'product__name',
        "product__product_marker",
        "user",
        "time_create",
    )

    ordering = ("-time_create",)

    def product_name(self, obj):
        return obj.product.name

    product_name.short_description = "Название продукта"

    def product_marker(self, obj):
        return obj.product.product_marker

    product_marker.short_description = "Маркетплейс"

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("product", "user")

    def has_change_permission(self, request, obj=...):
        return False
        # return super().has_change_permission(request, obj)


admin.site.register(UserProducts, UserProductsAdmin)
