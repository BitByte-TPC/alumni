# Refer Here : https://docs.celeryq.dev/en/stable/django/first-steps-with-django.html

import os

from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AlumniConnect.settings.development')

app = Celery('AlumniConnect')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes (no need to convert
# configuration object to byte stream since it can just pass the
# `django.conf:settings` string to child processes).
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send-birthday-wishes': {
        'task': 'applications.alumniprofile.tasks.send_birthday_wishes',
        'schedule': crontab(hour=13, minute=5),
    },
}

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
