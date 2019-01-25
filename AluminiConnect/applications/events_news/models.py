from django.db import models
import datetime, os
from time import strftime


def upload_event_photo(instance, filename):
    name, extension = os.path.splitext(filename)
    return "Events/" + str(instance.title) + extension

class Event(models.Model):
    event_id = models.AutoField(primary_key = True)
    title = models.TextField(max_length = 500)
    start_date = models.DateTimeField(default = datetime.datetime.now() + datetime.timedelta(hours=24))
    end_date = models.DateTimeField(default = datetime.datetime.now() + datetime.timedelta(hours=48))
    picture = models.ImageField(null = True, blank = True, upload_to = upload_event_photo)
    location = models.CharField(max_length = 100, null = True)
    address = models.TextField(max_length = 1000, default = "")
    description = models.TextField(default = "", null = True)

    def __str__(self):
        return self.title
