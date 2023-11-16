from django.core.mail import send_mail


def send(user_email):
    send_mail(
        'Тестовое письмо рассылки.',
        'Отправлено исправленное письмо в baground task.',
        'vladimir.papin@gmail.com',
        [user_email],
        fail_silently=False
    )
