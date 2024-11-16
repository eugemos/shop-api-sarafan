from django.contrib.auth.models import AbstractUser
# from django.db import models


class User(AbstractUser):
    class Meta:
        ordering = ('id',)
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
