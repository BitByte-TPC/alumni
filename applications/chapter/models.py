import os
from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from applications.alumniprofile.models import Profile
from applications.events_news.models import Event
from applications.gallery.models import Album


def upload_photo(instance, filename):
    name, extension = os.path.splitext(filename)
    return 'Chapter_Walls/' + str(instance.name) + ".jpg"


class Constants:
    POST = (
        ('President', 'President'),
        ('Hon. Secretary', 'Hon. Secretary'),
        ('Treasurer', 'Treasurer'),
        ('Other', 'Other')
    )


class Chapters(models.Model):
    name = models.CharField(max_length=100)
    description = RichTextUploadingField(blank=True, null=True)
    wall_picture = models.ImageField(null=True, blank=True, upload_to=upload_photo)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ChapterTeam(models.Model):
    chapter = models.ForeignKey(Chapters, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    post = models.CharField(choices=Constants.POST, max_length=50)
    other_post = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return 'Chapter: ' + str(self.chapter) + ' User: ' + str(self.user) + ' Post: ' + str(self.post)


class ChapterEvent(models.Model):
    chapter = models.ForeignKey(Chapters, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('chapter', 'event'),)

    def __str__(self):
        return 'Chapter: ' + str(self.chapter) + ' Event: ' + str(self.event)


class ChapterAlbum(models.Model):
    chapter = models.ForeignKey(Chapters, on_delete=models.CASCADE)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('chapter', 'album'),)

    def __str__(self):
        return 'Chapter: ' + str(self.chapter) + ' Event: ' + str(self.album)
