import uuid
from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField


class Publication(models.Model):
    title = RichTextField()
    description = RichTextUploadingField()
    thumb = ProcessedImageField(upload_to='Publications', processors=[ResizeToFit(300)], format='JPEG',
                                options={'quality': 90})
    tags = RichTextField()
    by = RichTextField()
    is_visible = models.BooleanField(default=True)
    created = models.DateTimeField()
    modified = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=255, unique=True)

    # def get_absolute_url(self):
    #    return reverse('album', kwargs={'slug':self.slug})

    def __str__(self):
        return self.title_stripped

    @property
    def title_stripped(self):
        from django.utils.html import strip_tags
        return strip_tags(self.title)


class PublicationMedia(models.Model):
    media = models.FileField(upload_to="files")
    publication = models.ForeignKey('publication', on_delete=models.PROTECT)
    alt = models.CharField(max_length=255, default=uuid.uuid4)
    created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=255, default=uuid.uuid4, editable=False)
