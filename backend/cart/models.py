from django.contrib.auth import get_user_model
from django.db import models

from products.models import Product


class ProductInCart(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        verbose_name='пользователь',
        on_delete=models.CASCADE,
        related_name='products_in_cart',
    )
    product = models.ForeignKey(
        Product,
        verbose_name='товар',
        on_delete=models.CASCADE,
        related_name='in_cart_of_users',
    )
    amount = models.PositiveIntegerField('количество')

    class Meta:
        verbose_name = 'товар в корзине'
        verbose_name_plural = 'товары в корзине'
