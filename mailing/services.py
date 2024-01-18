from datetime import datetime, timedelta
import pytz
from django.core.cache import cache
from django.core.mail import send_mail
from django.conf import settings
from mailing.models import Mailing, Logs
from users.services import send_sms, send_mail_user


def my_job():
    day = timedelta(days=1)
    weak = timedelta(days=7)
    month = timedelta(days=28)

    mailings = Mailing.objects.all().filter(is_activated=True)

    today = datetime.now(pytz.timezone('Europe/Moscow'))
    mailings = mailings.filter(next_date__lte=today)

    for mailing in mailings:
        if mailing.status != 'finished':
            mailing.status = 'active'
            mailing.save()
            emails_list = [client.email for client in mailing.mail_to.all()]

            result = send_mail_user(
                subject=mailing.message.topic,
                message=mailing.message.content,
                email_list=emails_list,
            )

            status = result == 1

            log = Logs(mailing=mailing, status=status)
            log.save()

            if status:  # на случай сбоя рассылки она останется активной
                if mailing.next_date < mailing.end_date:
                    mailing.status = 'created'
                else:
                    mailing.status = 'finished'

            if mailing.interval == 'daily':
                mailing.next_date = log.last_mailing_time + day
            elif mailing.interval == 'weekly':
                mailing.next_date = log.last_mailing_time + weak
            elif mailing.interval == 'monthly':
                mailing.next_date = log.last_mailing_time + month
            elif mailing.interval == 'once':
                mailing.next_date = mailing.end_date

            mailing.save()
            print(f'Рассылка {mailing.name} отправлена')
            #Рассылка по СМС/ не проверял на реальном номере
            phone_list = []
            for client in mailing.mail_to.all():
                if client.phone:
                    phone_list.append(client.phone)
            phone_str = '+'.join(phone_list)
            print(phone_str)
            sms_result = send_sms(phone=phone_str, message=mailing.message.content)
            print(f'СМС - {sms_result["status"]}')


def get_cache_mailing_count():
    if settings.CACHE_ENABLED:
        key = 'mailings_count'
        mailings_count = cache.get(key)
        if mailings_count is None:
            mailings_count = Mailing.objects.all().count()
            cache.set(key, mailings_count)
    else:
        mailings_count = Mailing.objects.all().count()
    return mailings_count


def get_cache_mailing_active():
    if settings.CACHE_ENABLED:
        key = 'active_mailings_count'
        active_mailings_count = cache.get(key)
        if active_mailings_count is None:
            active_mailings_count = Mailing.objects.filter(is_activated=True).count()
            cache.set(key, active_mailings_count)
    else:
        active_mailings_count = Mailing.objects.filter(is_activated=True).count()
    return active_mailings_count
