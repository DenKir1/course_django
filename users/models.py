from django.contrib.auth.models import AbstractUser
from django.db import models


NULLABLE = {'blank': True, 'null': True}
ACTIVE_CHOICES = [
    (True, 'Активен'),
    (False, 'Неактивен'),
]


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Почта')
    avatar = models.ImageField(upload_to='user/', verbose_name='Аватар', **NULLABLE)
    verify_code = models.CharField(max_length=15, verbose_name='Код верификации', **NULLABLE)
    verify_pass = models.CharField(max_length=15, verbose_name='Проверка кода', **NULLABLE)
    is_active = models.BooleanField(default=True, choices=ACTIVE_CHOICES, verbose_name='Активность')
    is_verify = models.BooleanField(default=False, choices=ACTIVE_CHOICES, verbose_name='Верифицирован')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        permissions = [
            ('set_is_active', 'Может блокировать пользователя')
        ]
