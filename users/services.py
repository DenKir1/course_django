import os
import requests
from django.conf import settings
from django.core.mail import send_mail


def send_sms(phone='79998887766', message='HOHO'):
    try:
        phone = phone.replace(' ', '+')
        message = message.replace(' ', '+')
        ID_SMS_RU = os.getenv('ID_SMS_RU')
        url = f'https://sms.ru/sms/send?api_id={ID_SMS_RU}&to={phone}&msg={message}&json=1'
        response = requests.get(url=url).json()
        print(f'СМС отправлено, статус - {response["status"]}')
        return response
    except requests.exceptions.ConnectionError:
        print('No connection')
        return {"status": False}


def send_mail_user(subject='', message='', email_list=''):
    try:
        result = send_mail(
            subject=f'{subject}',
            message=f'{message}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=email_list
        )
        print(f'Рассылка {email_list} прошла успешно')
        return result == 1
    except Exception as exc:
        print(f'Ошибка при отправке почты - {exc}')
        return False
