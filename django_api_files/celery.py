import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_api_files.settings')

app = Celery('django_api_files')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
