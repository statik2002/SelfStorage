from SelfStorage.celery import app

from .models import Rent, RemindDay, Status
from .service import send
from datetime import datetime, timedelta


@app.task
def send_email(email_detail):
    send(email_detail)


def serilaize_remind(remind_rent, check_day):
    check_day = check_day.replace('Хранение ', '')
    storage_tetx = f'подходит к концу, {check_day}' \
        if check_day == 'просрочен' else check_day.lower()
    return {
        'email': remind_rent.renter.email,
        'subject': f'Срок хранения Вашего бокса "{remind_rent.box.title}" '
                   f'{storage_tetx}',
        'message':
            f'Уважаемый {remind_rent.renter.first_name} '
            f'{remind_rent.renter.last_name}.\n'
            f'Срок хранения Вашего бокса "{remind_rent.box.title}" '
            f'{storage_tetx}.\n\n'
            f'Склад "{remind_rent.box.storage.title}"\n'
            f'Город: {remind_rent.box.storage.city}, '
            f'по адресу: {remind_rent.box.storage.address}.\n\n'
            f'Телефон для связи: '
            f'{remind_rent.box.storage.phone.as_international}'
    }


@app.task
def check_storage_life():
    remind_set_days = RemindDay.objects.all().select_related('status')
    check_days = {}
    for remind_set_day in remind_set_days:
        check_days[remind_set_day.day] = remind_set_day.status.title

    for check_day in check_days.keys():
        remind_rents = Rent.objects\
            .filter(end_date=(datetime.today() + timedelta(check_day)))\
            .select_related('renter')\
            .select_related('box__storage')

        status = Status.objects.get(title=check_days[check_day])
        for remind_rent in remind_rents:
            if remind_rent.status.title.find('закон') > 0:
                continue

            send_email(serilaize_remind(remind_rent, check_days[check_day]))
            remind_rent.status = status
            remind_rent.save()

    remind_rents = Rent.objects\
        .filter(end_date__lte=(datetime.today()))\
        .select_related('renter')\
        .select_related('box__storage')

    status = Status.objects.get(title='Просрочен')
    for remind_rent in remind_rents:
        if remind_rent.status.title.find('закон') > 0:
            continue

        send_email(serilaize_remind(remind_rent, 'Просрочен'))
        remind_rent.status = status
        remind_rent.save()
