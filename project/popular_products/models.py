from django.db import models

from main.models import Products

# Create your models here.


class ChannelLink(models.Model):
    name = models.CharField("Название", max_length=255)
    channel_id = models.CharField("ID канала", max_length=255)

    class Meta:
        managed = False
        db_table = "channel_links"
        verbose_name = "Канал"
        verbose_name_plural = "Каналы"

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField("Название", max_length=255)
    parent = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, blank=True, default=None
    )
    channel_links = models.ManyToManyField(
        ChannelLink, through="CategoryChannelLink", related_name="categories"
    )

    class Meta:
        managed = False
        db_table = "categories"
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        _name = self.name

        if self.parent is not None:
            _name = f"({self.parent.name}) {_name}"

        return _name


class CategoryChannelLink(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    channel_link = models.ForeignKey(ChannelLink, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = "category_channel_association"
        unique_together = ("category", "channel_link")


class PopularProduct(models.Model):
    product = models.ForeignKey(
        Products, on_delete=models.CASCADE, related_name="popular_products"
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="popular_products"
    )
    start_price = models.IntegerField()
    actual_price = models.IntegerField()
    sale = models.IntegerField()
    link = models.URLField(
        max_length=500
    )  # или models.CharField, если ссылка может быть невалидной
    time_create = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "popular_products"
        verbose_name = "Популярный товар"
        verbose_name_plural = "Популярные товары"

    def __str__(self):
        return f"{self.product} | {self.category}"
