# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AlembicVersion(models.Model):
    version_num = models.CharField(primary_key=True, max_length=32)

    class Meta:
        managed = False
        db_table = "alembic_version"


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = "auth_group"


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey("AuthPermission", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "auth_group_permissions"
        unique_together = (("group", "permission"),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey("DjangoContentType", models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = "auth_permission"
        unique_together = (("content_type", "codename"),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "auth_user"


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "auth_user_groups"
        unique_together = (("user", "group"),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "auth_user_user_permissions"
        unique_together = (("user", "permission"),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey(
        "DjangoContentType", models.DO_NOTHING, blank=True, null=True
    )
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "django_admin_log"


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = "django_content_type"
        unique_together = (("app_label", "model"),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "django_migrations"


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "django_session"


class OzonProducts(models.Model):
    link = models.CharField(blank=True, null=True)
    short_link = models.CharField(blank=True, null=True)
    start_price = models.FloatField(blank=True, null=True)
    actual_price = models.FloatField(blank=True, null=True)
    sale = models.FloatField(blank=True, null=True)
    name = models.CharField(blank=True, null=True)
    time_create = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey("Users", models.DO_NOTHING, blank=True, null=True)
    basic_price = models.FloatField(blank=True, null=True)
    ozon_punkt = models.ForeignKey(
        "OzonPunkts", models.DO_NOTHING, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "ozon_products"


class OzonPunkts(models.Model):
    index = models.BigIntegerField(blank=True, null=True)
    city = models.CharField(blank=True, null=True)
    zone = models.BigIntegerField(blank=True, null=True)
    time_create = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey("Users", models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "ozon_punkts"


class ProductPrices(models.Model):
    product = models.ForeignKey("Products", models.DO_NOTHING, blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    time_price = models.DateTimeField(blank=True, null=True)
    city = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "product_prices"


class Products(models.Model):
    product_marker = models.CharField(blank=True, null=True)
    name = models.CharField(blank=True, null=True)
    short_link = models.CharField(unique=True, blank=True, null=True)
    seller = models.CharField(blank=True, null=True)
    rate = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "products"
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    def __str__(self):
        return self.name


class Punkts(models.Model):
    index = models.BigIntegerField(blank=True, null=True)
    city = models.CharField(blank=True, null=True)
    wb_zone = models.BigIntegerField(blank=True, null=True)
    ozon_zone = models.BigIntegerField(blank=True, null=True)
    time_create = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey("Users", models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "punkts"


class Subscriptions(models.Model):
    name = models.CharField(blank=True, null=True)
    wb_product_limit = models.IntegerField(blank=True, null=True)
    ozon_product_limit = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "subscriptions"

    def __str__(self):
        return self.name


class UserJob(models.Model):
    job_id = models.CharField(blank=True, null=True)
    user = models.ForeignKey("Users", models.DO_NOTHING, blank=True, null=True)
    product_id = models.IntegerField(blank=True, null=True)
    product_marker = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "user_job"


class UserProductJob(models.Model):
    job_id = models.CharField(blank=True, null=True)
    user_product = models.ForeignKey(
        "UserProducts", models.DO_NOTHING, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "user_product_job"


class UserProducts(models.Model):
    product = models.ForeignKey(
        Products, models.DO_NOTHING, verbose_name="Продукт", blank=True, null=True
    )
    user = models.ForeignKey(
        "Users", models.DO_NOTHING, verbose_name="Пользователь", blank=True, null=True
    )
    link = models.CharField("Ссылка", blank=True, null=True)
    start_price = models.IntegerField("Начальная цена", blank=True, null=True)
    actual_price = models.IntegerField("Актуальная цена", blank=True, null=True)
    sale = models.IntegerField("Скидка", blank=True, null=True)
    time_create = models.DateTimeField("Время добавления", blank=True, null=True)

    class Meta:
        managed = False
        db_table = "user_products"
        verbose_name = "Продукт пользователя"
        verbose_name_plural = "Продукты пользователей"


class Users(models.Model):
    tg_id = models.BigAutoField(primary_key=True)
    username = models.CharField(blank=True, null=True)
    first_name = models.CharField(blank=True, null=True)
    last_name = models.CharField(blank=True, null=True)
    time_create = models.DateTimeField("Время добавления", blank=True, null=True)
    last_action = models.CharField(blank=True, null=True)
    last_action_time = models.DateTimeField(blank=True, null=True)
    subscription = models.ForeignKey(
        Subscriptions,
        on_delete=models.DO_NOTHING,
        verbose_name="Подписка",
        blank=True,
        null=True,
    )
    utm_source = models.CharField("UTM метка", blank=True, null=True)
    is_active = models.BooleanField("Активный?", default=True)
    wb_total_count = models.IntegerField("Товары WB за всё время", db_default=0)
    ozon_total_count = models.IntegerField("Товары OZON за всё время", db_default=0)

    class Meta:
        managed = False
        db_table = "users"
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f"Пользователь - ID {self.tg_id} {self.username}"


class UTM(models.Model):
    keitaro_id = models.CharField(max_length=255, blank=True, null=True)
    utm_source = models.CharField(max_length=255, blank=True, null=True)
    utm_medium = models.CharField(max_length=255, blank=True, null=True)
    utm_campaign = models.CharField(max_length=255, blank=True, null=True)
    utm_content = models.CharField(max_length=255, blank=True, null=True)
    utm_term = models.CharField(max_length=255, blank=True, null=True)
    banner_id = models.CharField(max_length=255, blank=True, null=True)
    campaign_name = models.CharField(max_length=255, blank=True, null=True)
    campaign_name_lat = models.CharField(max_length=255, blank=True, null=True)
    campaign_type = models.CharField(max_length=255, blank=True, null=True)
    campaign_id = models.CharField(max_length=255, blank=True, null=True)
    creative_id = models.CharField(max_length=255, blank=True, null=True)
    device_type = models.CharField(max_length=255, blank=True, null=True)
    gbid = models.CharField(max_length=255, blank=True, null=True)
    keyword = models.CharField(max_length=255, blank=True, null=True)
    phrase_id = models.CharField(max_length=255, blank=True, null=True)
    coef_goal_context_id = models.CharField(max_length=255, blank=True, null=True)
    match_type = models.CharField(max_length=255, blank=True, null=True)
    matched_keyword = models.CharField(max_length=255, blank=True, null=True)
    adtarget_name = models.CharField(max_length=255, blank=True, null=True)
    adtarget_id = models.CharField(max_length=255, blank=True, null=True)
    position = models.CharField(max_length=255, blank=True, null=True)
    position_type = models.CharField(max_length=255, blank=True, null=True)
    source = models.CharField(max_length=255, blank=True, null=True)
    source_type = models.CharField(max_length=255, blank=True, null=True)
    region_name = models.CharField(max_length=255, blank=True, null=True)
    region_id = models.CharField(max_length=255, blank=True, null=True)
    yclid = models.CharField(max_length=255, blank=True, null=True)
    client_id = models.CharField(max_length=255, blank=True, null=True)
    user = models.OneToOneField(Users, on_delete=models.CASCADE, related_name="utm")

    class Meta:
        db_table = "utms"
        managed = False

    def __str__(self):
        return f"{self.user.tg_id} {self.keitaro_id} {self.source}"


class WbProducts(models.Model):
    link = models.CharField(blank=True, null=True)
    short_link = models.CharField(blank=True, null=True)
    start_price = models.FloatField(blank=True, null=True)
    actual_price = models.FloatField(blank=True, null=True)
    sale = models.FloatField(blank=True, null=True)
    name = models.CharField(blank=True, null=True)
    time_create = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey(Users, models.DO_NOTHING, blank=True, null=True)
    wb_punkt = models.ForeignKey("WbPunkts", models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "wb_products"


class WbPunkts(models.Model):
    zone = models.BigIntegerField(blank=True, null=True)
    time_create = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey(Users, models.DO_NOTHING, blank=True, null=True)
    index = models.BigIntegerField(blank=True, null=True)
    city = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "wb_punkts"


# class PopularProduct(models.Model):
#     product = models.ForeignKey(
#         Products,
#         on_delete=models.CASCADE,
#         related_name='popular_products'
#     )
#     category = models.ForeignKey(
#         'Category',
#         on_delete=models.CASCADE,
#         related_name='popular_products'
#     )
#     start_price = models.IntegerField()
#     actual_price = models.IntegerField()
#     sale = models.IntegerField()
#     link = models.URLField(max_length=500)  # или models.CharField, если ссылка может быть невалидной
#     time_create = models.DateTimeField()

#     def __str__(self):
#         return f"{self.product} | {self.actual_price}"

# class ChannelLink(models.Model):
#     name = models.CharField('Название', max_length=255)
#     channel_id = models.CharField('ID канала', max_length=255)

#     class Meta:
#         managed = False
#         db_table = 'channel_links'
#         verbose_name = 'Канал'
#         verbose_name_plural = 'Каналы'

#     def __str__(self):
#         return self.name


# class Category(models.Model):
#     name = models.CharField('Название', max_length=255)
#     parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, default=None)
#     channel_links = models.ManyToManyField(ChannelLink, through='CategoryChannelLink', related_name='categories')

#     class Meta:
#         managed = False
#         db_table = 'categories'
#         verbose_name = 'Категория'
#         verbose_name_plural = 'Категории'

#     def __str__(self):
#         _name = self.name

#         if self.parent is not None:
#             _name = f'({self.parent.name}) {_name}'

#         return _name


# class CategoryChannelLink(models.Model):
#     category = models.ForeignKey(Category, on_delete=models.CASCADE)
#     channel_link = models.ForeignKey(ChannelLink, on_delete=models.CASCADE)

#     class Meta:
#         managed = False
#         db_table = 'category_channel_association'
#         unique_together = ('category', 'channel_link')
