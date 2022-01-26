# Refer Here : https://realpython.com/asynchronous-tasks-with-django-and-celery/

from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AluminiConnect.settings')
app = Celery("AluminiConnect")

app.config_from_object("django.conf:settings")
app.autodiscover_tasks(lambda : settings.INSTALLED_APPS)

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))