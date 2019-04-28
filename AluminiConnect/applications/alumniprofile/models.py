from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
import datetime, os
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from model_utils import FieldTracker
from time import strftime
from .funcs import send_verification_email
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
        ('PhD', 'PhD')
    )

    BRANCH = (
        ('CSE', 'Computer Science and Engineering'),
        ('ECE', 'Electronics and Communication Engineering'),
        ('ME', 'Mechanical Engineering'),
        ('NS', 'Natural Sciences'),
        ('MT', 'Mechatronics'),
        ('DS', 'Design'),
        ('NA', 'Not Applicable')
    )

    WORKING_STATUS = (
        ('Is Working', 'Is Working'),
        ('Is Pursuing Higher Studies', 'Is Pursuing Higher Studies'),
        ('Is Self Employed', 'Is Self Employed')
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
    email = models.EmailField(null = False, default="")
    alternate_email = models.EmailField(null = True, blank = True)
    year_of_admission = models.IntegerField(null = True)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    name = models.CharField(max_length = 500, default="", null = False)
    fathers_name = models.CharField(max_length=500, default="")
    programme = models.CharField(max_length = 50, choices = Constants.PROG_CHOICES, null = False)
    branch = models.CharField(choices = Constants.BRANCH, max_length = 20, null = False)
    sex = models.CharField(max_length = 2, choices = Constants.SEX_CHOICES, default = 'M')
    date_of_birth = models.DateField(default = datetime.date(1970,1,1))
    current_address = models.TextField(max_length = 1000, default = "")
    permanent_address = models.TextField(max_length = 1000, blank = True, null=True)
    mobile1 = models.BigIntegerField(null = True)
    mobile2 = models.BigIntegerField(null = True, blank = True)
    phone_no = models.BigIntegerField(null = True, blank=True)
    working_status = models.CharField(max_length=50 ,choices=Constants.WORKING_STATUS, default = '1', null = False)
    current_position = models.CharField(max_length = 128, null=True, blank = True)
    current_organisation = models.CharField(max_length = 128, null=True, blank = True)
    past_experience = models.IntegerField(null = True, blank = True)
    current_course = models.CharField(null = True, blank = True, max_length = 128)
    current_university = models.CharField(null = True, blank = True, max_length = 128)
    city = models.CharField(null = True, max_length = 20, blank=True)
    country = models.CharField(null = True, max_length = 20, blank=True)
    state = models.CharField(null = True, max_length = 20, blank=True)
    facebook = models.URLField(default = "www.facebook.com")
    linkedin = models.URLField(null = True, blank = True, default = "www.linkedin.com")
    website = models.URLField(null = True, blank = True )
    profile_picture = models.ImageField(null = True, upload_to = upload_photo)
    is_verified = models.BooleanField(default=True)
    date_of_joining = models.DateField(null = True, blank = True)
    reg_no = models.BigIntegerField(null=True, default=0, editable=False)
    mail_sent = models.BooleanField(default=False)
    mail_sent_tracker = FieldTracker(fields=['mail_sent'])
    def __str__(self):
        return self.name

@receiver(post_save, sender=Profile)
def check(sender, instance, created, update_fields, **kwargs):
    if instance.mail_sent_tracker.has_changed('mail_sent') and instance.mail_sent_tracker.previous('mail_sent') == False: #Alumni Verified
        print("Mail Sent to {}".format(instance.name), send_verification_email(instance.name, instance.email, instance.year_of_admission, instance.batch, instance.programme, instance.branch, instance.reg_no))