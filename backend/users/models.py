from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class Meta:
        ordering = ('id',)
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
