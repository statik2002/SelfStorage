import os

from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SelfStorage.settings')

app = Celery('SelfStorage')

app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


app.conf.beat_schedule = {
    # Executes every day at  10:00 am. use crontab(minute=0, hour=10)
    # Executes every minutes use crontab(minute='*/1')
    'check-storage-life-and-send-email': {
        'task': 'main.tasks.check_storage_life',
        'schedule': crontab(minute=0, hour=10),
    },
}
