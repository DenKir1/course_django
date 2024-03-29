# Generated by Django 5.0 on 2024-01-18 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='verify_pass',
        ),
        migrations.AddField(
            model_name='user',
            name='phone',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Телефон'),
        ),
        migrations.AddField(
            model_name='user',
            name='verify_phone',
            field=models.CharField(blank=True, max_length=15, null=True, verbose_name='Код верификации телефона'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(choices=[(True, 'Активен'), (False, 'Неактивен')], default=False, verbose_name='Почта активирована'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_verify',
            field=models.BooleanField(choices=[(True, 'Активен'), (False, 'Неактивен')], default=False, verbose_name='Номер телефона верифицирован'),
        ),
        migrations.AlterField(
            model_name='user',
            name='verify_code',
            field=models.CharField(blank=True, max_length=15, null=True, verbose_name='Код верификации почты'),
        ),
    ]
