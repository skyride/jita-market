import os

from celery import Celery
from django.conf import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jita.settings')
app = Celery("jita")
app.config_from_object('django.conf:settings')
app.autodiscover_tasks()
