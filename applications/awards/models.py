from django.db import models
import datetime
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField


# Create your models here.

class Award(models.Model):
    award_id = models.AutoField(primary_key=True)
    title = RichTextField()
    by = models.CharField(max_length=255, null=True)
    description = RichTextUploadingField()
    published_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

    @property
    def title_stripped(self):
        from django.utils.html import strip_tags
        return strip_tags(self.title)
