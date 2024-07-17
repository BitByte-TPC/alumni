from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField
from django.utils.html import strip_tags
from django.core.validators import MaxLengthValidator
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit

class Award(models.Model):
    award_id = models.AutoField(primary_key=True)
    title = RichTextField()
    by = models.CharField(max_length=255, null=True)
    received_by = models.CharField(max_length=255, null=True, blank=True)
    description = RichTextUploadingField(validators=[MaxLengthValidator(2000)])
    image = ProcessedImageField(
        upload_to='awards/images/',
        processors=[ResizeToFit(300, 300)],
        format='JPEG',
        options={'quality': 90},
        null=True,
        blank=True
    )
    published_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

    @property
    def title_stripped(self):
        return strip_tags(self.title)

    @property
    def description_snippet(self):
        return ' '.join(strip_tags(self.description).split()[:50]) + ('...' if len(strip_tags(self.description).split()) > 50 else '')