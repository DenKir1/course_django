from django.db import models
from django.utils import timezone

import users.models

NULLABLE = {'null': True, 'blank': True}

STATUS_CHOICES = [
    ('created', 'Создана'),
    ('active', 'Запущена'),
    ('finished', 'Завершена'),
]
INTERVAL_CHOICES = [
    ('once', 'разовая'),
    ('daily', 'ежедневно'),
    ('weekly', 'раз в неделю'),
    ('monthly', 'раз в месяц'),
]
ACTIVE_CHOICES = [
    (True, 'Активна'),
    (False, 'Неактивна'),
]
LOG_CHOICES = [
    (True, 'Успешно'),
    (False, 'Неудача'),
]


class Client(models.Model):
    full_name = models.CharField(max_length=150, verbose_name='ФИО')
    email = models.EmailField(unique=True, verbose_name='Почта')
    phone = models.CharField(max_length=20, verbose_name='Телефон', **NULLABLE)
    comment = models.TextField(verbose_name='Комментарий', **NULLABLE)
    owner = models.ForeignKey(users.models.User, on_delete=models.CASCADE, null=True, verbose_name='Отправитель')

    def __str__(self):
        return f'{self.email}'

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'
        permissions = [
            ('client_delete', 'Может удалять клиентов')
        ]


class Message(models.Model):
    topic = models.CharField(max_length=250, verbose_name='Тема')
    content = models.TextField(verbose_name='Содержание')
    owner = models.ForeignKey(users.models.User, on_delete=models.CASCADE, null=True, verbose_name='Владелец сообщения')

    def __str__(self):
        return self.topic

    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщения'


class Mailing(models.Model):
    name = models.CharField(max_length=50, verbose_name='Рассылка')
    mail_to = models.ManyToManyField(Client, verbose_name='Получатели')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='Сообщение', **NULLABLE)
    start_date = models.DateTimeField(default=timezone.now, verbose_name='Начало рассылки')
    next_date = models.DateTimeField(default=timezone.now, verbose_name='Следующая рассылка')
    end_date = models.DateTimeField(verbose_name='Конец рассылки')
    interval = models.CharField(default='once', max_length=10, choices=INTERVAL_CHOICES, verbose_name='Периодичность')
    status = models.CharField(default='created', max_length=10, choices=STATUS_CHOICES, verbose_name='Статус')
    owner = models.ForeignKey(users.models.User, on_delete=models.CASCADE, null=True, verbose_name='Владелец рассылки')

    is_activated = models.BooleanField(default=True, choices=ACTIVE_CHOICES, verbose_name='Активность')

    def __str__(self):
        return f'"{self.name}"'

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'
        ordering = ('start_date',)

        permissions = [
            ('set_is_activated', 'Может отключать рассылку'),
            ('can_view', 'Может просматривать рассылки')
        ]


class Logs(models.Model):
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='Рассылка', **NULLABLE)
    last_mailing_time = models.DateTimeField(auto_now=True, verbose_name='Время рассылки', **NULLABLE)
    status = models.CharField(default=False, max_length=10, choices=LOG_CHOICES, verbose_name='Попытка', **NULLABLE)

    def __str__(self):
        return f'{self.last_mailing_time} - {self.status}'

    class Meta:
        verbose_name = 'Лог сообщения'
        verbose_name_plural = 'Логи сообщений'
