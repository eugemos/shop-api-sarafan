from django.contrib import admin
from django.db import models

from categories.models import Subcategory


class Product(models.Model):
    name = models.CharField('наименование', max_length=150)
    slug = models.SlugField('обозначение', unique=True)
    price = models.PositiveIntegerField('цена')
    subcategory = models.ForeignKey(
        Subcategory,
        verbose_name='подкатегория',
        on_delete=models.PROTECT,
        related_name='products',
    )

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self):
        return self.name

    @property
    @admin.display(description='категория')
    def category(self):
        return self.subcategory.category


class ProductImage(models.Model):
    IMAGES_UPLOAD_PATH = 'products/'

    image = models.ImageField(
        'изображение',
        upload_to=IMAGES_UPLOAD_PATH,
        blank=True,
        null=True,
    )
    product = models.ForeignKey(
        Product,
        verbose_name='товар',
        on_delete=models.CASCADE,
        related_name='images',
    )

    class Meta:
        verbose_name = 'изображение товара'
        verbose_name_plural = 'изображения товара'
