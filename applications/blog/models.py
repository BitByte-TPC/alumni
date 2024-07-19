import os
from django.db import models

from multiselectfield import MultiSelectField
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
# Create your models here.
class Constants:
    TAGS = (
        ('Food', 'Food'),
        ('Technology', 'Technology'),
        ('Industry', 'Industry'),
        ('College', 'College')
    )

    TYPE = (
        ('S', 'Self'),
        ('C', 'Campaign')
    )

def upload_photo(instance, filename):
    name, extension = os.path.splitext(filename)
    return 'Profile_Pictures/' + str(instance.blog_id) + ".jpg"

class Campaign(models.Model):
    campaign_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250)
    date_started = models.DateTimeField(auto_now=True)
    date_ended = models.DateTimeField(blank=True, null=True)
    thumbnail = models.ImageField(null=True, upload_to=upload_photo,blank=True)
    description = models.TextField(blank=False, max_length=2000)

    def __str__(self):
        return self.name

class Blog(models.Model):
        blog_id = models.AutoField(primary_key=True)
        author = models.ForeignKey(User, on_delete=models.CASCADE)
        title = models.CharField(max_length=250, blank=False)

        thumbnail = models.ImageField(null=True, upload_to=upload_photo)
        tags = MultiSelectField(choices=Constants.TAGS, max_choices=5, max_length=50 )
        content = models.TextField(max_length=2000, blank=False)
        date_added = models.DateTimeField(auto_now=True)
        updated_at = models.DateTimeField(auto_now=True, null=True)
        upvotes = models.IntegerField(default=0)
        
        blog_type = models.CharField(choices=Constants.TYPE, max_length=15,default='S')
        campaign_id = models.ForeignKey(Campaign, on_delete=models.CASCADE, null=True, blank=True)
        approved = models.BooleanField(default=False)

        def __str__(self):
            return self.title

class Replies(models.Model):
    blog_id = models.ForeignKey(Blog, on_delete=models.CASCADE)
    reply_id = models.AutoField(primary_key=True)
    content = models.CharField(blank=False, max_length=500)

    time_stamp = models.DateTimeField(auto_now=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE,related_name='sender')
    receiver  = models.ForeignKey(User,on_delete=models.CASCADE,related_name='receiver',default='', blank=True,null=True)

