from django.db import models
import datetime, os
from time import strftime


def upload_to_photo(instance, filename):
    name, extension = os.path.splitext(filename)
    return str(instance.user.username) + "-photo-" + strftime("%Y_%m_%d-%H_%M_%S") + extension

class Event(models.Model):
    event_id = models.UUIDField(primary_key = True)
    title = models.TextField(max_length = 500)
    start_date = models.DateTimeField(default = datetime.datetime.now() + datetime.timedelta(hours=24))
    end_date = models.DateTimeField(default = datetime.datetime.now() + datetime.timedelta(hours=48))
    picture = models.ImageField(upload_to = "events_news/img")
    location = models.CharField(max_length = 100, null = True)
    address = models.TextField(max_length = 1000, default = "")
    description = models.TextField(default = "", null = True)
    photos = models.ImageField(upload_to = upload_to_photo)
