from django.core.mail import send_mail
from django.conf import settings


def send(email_detail):
    # Отправка письма
    #
    # Словарь email_detail:
    #   email - почта кому
    #   subject - тема письма
    #   message - текст письма

    send_mail(
        subject=email_detail['subject'],
        message=email_detail['message'],
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email_detail['email']],
        fail_silently=False
    )
