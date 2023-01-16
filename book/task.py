from django.core.mail import send_mail

from celery import shared_task


@shared_task()
def send_activation_code(activation_code, email):
    activation_link = f'http://127.0.0.1:8000/account/activate/{activation_code}'
    message = f'Пожалуйста нажмите на кнопочку активации "by Ice":\n{activation_link}'
    send_mail("Activate account", message, 'admin@admin.com', recipient_list=[email])