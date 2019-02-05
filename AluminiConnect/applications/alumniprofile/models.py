from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
import datetime, os
from django.db.models.signals import post_save
from django.dispatch import receiver

from time import strftime

class Constants:

    SEX_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    )

    PROG_CHOICES = (
        ('B.Tech', 'B.Tech'),
        ('B.Des', 'B.Des'),
        ('M.Des', 'M.Des'),
        ('M.Tech', 'M.Tech'),
        ('PHD', 'PHD')
    )

    BRANCH = (
        ('CSE', 'Computer Science and Engineering'),
        ('ECE', 'Electronics and Communication Engineering'),
        ('ME', 'Mechanical Engineering'),
        ('NS', 'Natural Sciences'),
        ('NA', 'Not Applicable')
    )


class Batch(models.Model):
    batch = models.IntegerField(primary_key= True)

    def __str__(self):
        return str(self.batch)

def upload_photo(instance, filename):
    name, extension = os.path.splitext(filename)
    return 'Profile_Pictures/' + str(instance.roll_no) + ".jpg"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    roll_no = models.IntegerField(primary_key = True)
    email = models.EmailField(null = False)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    first_name = models.CharField(max_length = 500, default="", null = False)
    last_name = models.CharField(max_length = 500, default="")
    programme = models.CharField(max_length = 50, choices = Constants.PROG_CHOICES, null = False)
    branch = models.CharField(choices = Constants.BRANCH, max_length = 20, null = False)
    sex = models.CharField(max_length = 2, choices = Constants.SEX_CHOICES, default = 'M')
    date_of_birth = models.DateField(default = datetime.date(1970,1,1))
    current_address = models.TextField(max_length = 1000, default = "")
    permanent_address = models.TextField(max_length = 1000, default = "")
    phone_no = models.BigIntegerField(null = True, default = 9999999999)
    current_city = models.CharField(null = True, max_length = 20)
    current_organisation = models.CharField(null = True, max_length = 20)
    current_university = models.CharField(null = True, max_length = 20)
    current_position = models.CharField(null = True, max_length = 128)
    linkedin = models.URLField(null=True)
    website = models.URLField(null = True, blank=True)
    profile_picture = models.ImageField(null = True, blank = True, upload_to = upload_photo)
    is_registered = models.BooleanField(default=False)

    def __str__(self):
        return self.first_name + " " + self.last_name
    
# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()