from django.db import models
import datetime, os
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User


def upload_event_photo(instance, filename):
    name, extension = os.path.splitext(filename)
    return "Events/" + str(instance.event_id) + extension

class Event(models.Model):
    event_id = models.AutoField(primary_key = True)
    title = RichTextField()
    start_date = models.DateTimeField(default = datetime.datetime(2019, 1, 1, 12, 0, 0))
    end_date = models.DateTimeField(default = datetime.datetime(2019, 1, 1, 12, 0, 0))
    by = models.CharField(max_length = 255, null=True)
    picture = models.ImageField(null = True, blank = True, upload_to = upload_event_photo)
    location = models.CharField(max_length = 100, null = True)
    address = RichTextUploadingField()
    description = RichTextUploadingField()

    def __str__(self):
        return self.title_stripped

    @property
    def is_completed(self):
        return (timezone.now() > self.end_date)
    
    @property
    def title_stripped(self):
       from django.utils.html import strip_tags
       return strip_tags(self.title)

class Attendees(models.Model):
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = (("event_id", "user_id"),)
