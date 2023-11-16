from SelfStorage.celery import app

from .models import Customer
from .service import send


@app.task
def send_email(user_email):
    send(user_email)


@app.task
def check_storage_life():
    for customer in Customer.objects.all():
        send(customer.email)
