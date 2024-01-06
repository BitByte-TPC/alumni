import uuid
from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField
from applications.events_news.models import Event


class Album(models.Model):
    title = RichTextField()
    description = RichTextUploadingField()
    thumb = ProcessedImageField(upload_to='Albums', processors=[ResizeToFit(300)], format='JPEG',
                                options={'quality': 90})
    tags = RichTextField()
    is_visible = models.BooleanField(default=True)
    created = models.DateTimeField()
    modified = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=255, unique=True)
    event_id = models.ForeignKey(Event, on_delete=models.PROTECT, null=True, blank=True)
    album_link = RichTextUploadingField(null=True, blank=True)

    # def get_absolute_url(self):
    #    return reverse('album', kwargs={'slug':self.slug})

    def __str__(self):
        return self.title_stripped

    @property
    def title_stripped(self):
        from django.utils.html import strip_tags
        return strip_tags(self.title)


class AlbumImage(models.Model):
    image = ProcessedImageField(upload_to='Albums', processors=[ResizeToFit(1280)], format='JPEG',
                                options={'quality': 70})
    thumb = ProcessedImageField(upload_to='Albums', processors=[ResizeToFit(300)], format='JPEG',
                                options={'quality': 80})
    album = models.ForeignKey('album', on_delete=models.CASCADE)
    alt = models.CharField(max_length=255, default=uuid.uuid4)
    created = models.DateTimeField(auto_now_add=True)
    width = models.IntegerField(default=0)
    height = models.IntegerField(default=0)
    slug = models.SlugField(max_length=255, default=uuid.uuid4, editable=False)
