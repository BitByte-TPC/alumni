from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
import datetime, os
from time import strftime

class Constants:

    SEX_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    )

    DISC_CHOICES = (
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
        ('NA', 'Not Applicable')
    )

def upload_photo(instance, filename):
    name, extension = os.path.splitext(filename)
    return 'Profile_Pictures/' + str(instance.user.first_name) +"_" + str(instance.user.last_name)+ ".jpg"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    roll_no = models.IntegerField(primary_key = True)
    batch = models.IntegerField(null = True)
    programme = models.CharField(max_length = 50, choices = Constants.DISC_CHOICES)
    branch = models.CharField(choices = Constants.BRANCH, max_length = 20)
    sex = models.CharField(max_length = 2, choices = Constants.SEX_CHOICES, default = 'M')
    date_of_birth = models.DateField(default = datetime.date(1970,1,1))
    address = models.TextField(max_length = 1000, default = "")
    phone_no = models.BigIntegerField(null = True, default = 9999999999)
    current_city = models.CharField(null = True, max_length = 20)
    current_organisation = models.CharField(null = True, max_length = 20)
    current_university = models.CharField(null = True, max_length = 20)
    current_position = models.CharField(null = True, max_length = 128)
    linkedin = models.URLField(null=True)
    website = models.URLField(null = True, blank=True)
    profile_picture = models.ImageField(null = True, blank = True, upload_to = upload_photo)
    last_visit = models.DateTimeField(default = datetime.datetime.now())

    def __str__(self):
        return self.user.username