from datetime import datetime, timedelta

from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count 

from .models import UserProducts, Users, Punkts, Products


@staff_member_required
def custom_admin_view(request, self=None):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    item_limit = 10

    today = datetime.now()

    selected_date = 'сегодня'

    if not start_date:
        start_of_time = today.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_time = today.replace(hour=23, minute=59, second=59, microsecond=999999)
    else:
        if not end_date:
            # selected_date = f'{start_date}'

            start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")

            selected_date = start_date_obj.strftime("%d.%m.%Y")

            start_of_time = start_date_obj.replace(hour=0, minute=0, second=0, microsecond=0)
            end_of_time = start_date_obj.replace(hour=23, minute=59, second=59, microsecond=999999)
        else:
            # selected_date = f'{start_date} - {end_date}'

            start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
            end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")

            start_selected_date = start_date_obj.strftime("%d.%m.%Y")
            end_selected_date = end_date_obj.strftime("%d.%m.%Y")

            selected_date = f'{start_selected_date} -> {end_selected_date}'

            start_of_time = start_date_obj.replace(hour=0, minute=0, second=0, microsecond=0)
            end_of_time = end_date_obj.replace(hour=23, minute=59, second=59, microsecond=999999)

    products_added = UserProducts.objects.select_related('product')\
                                                .filter(time_create__range=(start_of_time, end_of_time))\
                                                .values_list('product__product_marker', flat=True)
    
    users_added = Users.objects.filter(time_create__range=(start_of_time, end_of_time))

    popular_cities = Punkts.objects.values('city').annotate(city_count=Count('id')).order_by('-city_count')[:item_limit]

    # popular_products = UserProducts.objects.select_related('product', 'user').values('product').annotate(user_count=Count('user', distinct=True))\
    #                                                                         .order_by('-user_count')
    
    popular_products = Products.objects.annotate(user_count=Count('userproducts'))\
                                        .filter(user_count__gte=2)\
                                        .order_by('-user_count')[:item_limit]
    
    # for product in popular_products:
    #     print_dict = {
    #         'product_marker': product.product_marker,
    #         'name': product.name,
    #         'product_id': product.id,
    #         # 'city_count': product.city_count,
    #         'user_count': product.user_count,
    #     }
        # print(print_dict)

    # print(popular_cities)
    
    wb_count = ozon_count = 0

    for product_marker in products_added:
        if product_marker == 'wb':
            wb_count += 1
        else:
            ozon_count += 1

    context = {
        'wb_count': wb_count,
        'ozon_count': ozon_count,
        'user_count': len(users_added),
        'selected_date': selected_date,
        'start_date': start_date,
        'end_date': end_date,
        'popular_cities': popular_cities,
        'popular_products': popular_products,
        'page_name': 'Статистика',
        "app_list": self.get_app_list(request),
        **self.each_context(request),
    }

    return render(request, 'admin/custom_admin_page.html', context)