from django.db import models
import datetime, os
from time import strftime


def upload_news_photo(instance, filename):
    name, extension = os.path.splitext(filename)
    return "News/" + str(instance.news_id) + extension

class News(models.Model):
    news_id = models.AutoField(primary_key = True)
    title = models.TextField(max_length = 500)
    date = models.DateTimeField(default = datetime.datetime.now())
    by = models.TextField(max_length = 500)
    picture = models.ImageField(null = True, blank = True, upload_to = upload_news_photo)
    description = models.TextField(default = "", null = True)

    def __str__(self):
        return self.title
