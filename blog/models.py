from django.db import models
from mailing.models import NULLABLE


class Blog(models.Model):
    topic = models.CharField(max_length=250, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержание')
    preview = models.ImageField(upload_to='blog/preview/', verbose_name='Изображение', **NULLABLE)
    views_count = models.IntegerField(default=0, verbose_name='Просмотры')
    public_date = models.DateField(auto_now=True)

    def __str__(self):
        return self.topic

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'
