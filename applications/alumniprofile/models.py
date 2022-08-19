from asyncio import constants
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
import datetime, os
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from model_utils import FieldTracker
from time import strftime
from applications.adminportal.mail_helper import send_verification_email


class Constants:
    SEX_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    )

    ROLE_CHOICES = (
        ('S','Student'),
        ('A','Alumni'),
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
        ('SM', 'Smart Manufacturing'),
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

    EMPLOYMENT_TYPE = (
        ('ft', 'Full-time'),
        ('pt', 'Part-time'),
        ('se', 'Self-employed'),
        ('fr', 'Freelance'),
        ('in', 'Internship'),
        ('tr', 'Trainee'),
    )

    # For IIIT Jabalpur
    YEAR_OF_ADDMISSION = tuple((n, str(n)) for n in range(2005, datetime.datetime.now().year))

    # For Education (other than IIIT Jabalpur)
    ADMISSION_YEAR = tuple((n, str(n)) for n in range(1990, datetime.datetime.now().year + 1))

    PASSING_YEAR = tuple((n, str(n)) for n in range(1990, datetime.datetime.now().year + 1))


class Batch(models.Model):
    batch = models.IntegerField(primary_key=True)

    def __str__(self):
        return str(self.batch)


def upload_photo(instance, filename):
    name, extension = os.path.splitext(filename)
    return 'Profile_Pictures/' + str(instance.roll_no) + ".jpg"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=2, choices=Constants.ROLE_CHOICES, default='A')

    # Institute Details
    roll_no = models.CharField(primary_key=True, max_length=15)
    year_of_admission = models.IntegerField(null=True, choices=Constants.YEAR_OF_ADDMISSION)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, null=True)
    programme = models.CharField(max_length=1000, choices=Constants.PROG_CHOICES, null=False)
    branch = models.CharField(choices=Constants.BRANCH, max_length=1000, null=False)

    # Alumni Specific
    reg_no = models.BigIntegerField(null=True, default=0, editable=False)

    # Personal Details
    name = models.CharField(max_length=1000, default="", null=False)
    sex = models.CharField(max_length=2, choices=Constants.SEX_CHOICES, default='M')
    date_of_birth = models.DateField(default=datetime.date(1970, 1, 1))
    email = models.EmailField()
    alternate_email = models.EmailField(blank=True)
    fathers_name = models.CharField(max_length=1000, default="")
    spouse_name = models.CharField(null=True, blank=True, max_length=1000, default="")
    mobile1 = models.BigIntegerField(null=True)
    mobile2 = models.BigIntegerField(null=True, blank=True)
    phone_no = models.BigIntegerField(null=True, blank=True)
    current_address = models.TextField(max_length=1000, default="")
    permanent_address = models.TextField(max_length=1000, blank=True, null=True)
    city = models.CharField(null=True, max_length=1000, blank=True)
    state = models.CharField(null=True, max_length=1000, blank=True)
    country = models.CharField(null=True, max_length=1000, blank=True)
    profile_picture = models.ImageField(null=True, upload_to=upload_photo)

    # Experience & Higher Studies (for Alumni)
    working_status = models.CharField(max_length=1000, choices=Constants.WORKING_STATUS, blank=True)
    current_position = models.CharField(max_length=1000, null=True, blank=True)
    current_organisation = models.CharField(max_length=1000, null=True, blank=True)
    date_of_joining = models.DateField(null=True, blank=True, default=datetime.date.today)
    past_experience = models.IntegerField(null=True, blank=True)
    current_course = models.CharField(null=True, blank=True, max_length=1000)
    current_university = models.CharField(null=True, blank=True, max_length=1000)

    # Social
    linkedin = models.URLField(null=True, blank=True, default="www.linkedin.com")
    facebook = models.URLField(null=True, blank=True, default="www.facebook.com")
    instagram = models.CharField(null=True, blank=True, max_length=1000)
    website = models.URLField(null=True, blank=True)
    
    # User verification
    mail_sent = models.BooleanField(default=False)  # To be used to track if the email was actually sent.
    verify = models.BooleanField(null=True)
    mail_sent_tracker = FieldTracker(fields=['verify'])

    # Last edit
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.name


@receiver(post_save, sender=Profile)
def check(sender, instance, created, update_fields, **kwargs):
    if instance.mail_sent_tracker.has_changed('verify') and instance.mail_sent_tracker.previous(
            'verify') != True:  # Alumni Verified
        mail_sent = send_verification_email("alumni.iiitdmj.ac.in", True, instance)

        # Can use either of below methods.
        # Though, the bottom one is preferred.
        # sender.objects.filter(roll_no=instance.roll_no).update(mail_sent=mail_sent)

        post_save.disconnect(check, Profile)
        instance.mail_sent = mail_sent
        instance.save()
        post_save.connect(check, Profile)


class PastExperience(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    position = models.CharField(max_length=1000)
    emp_type = models.CharField(max_length=10, choices=Constants.EMPLOYMENT_TYPE)
    organisation = models.CharField(verbose_name='Company/Org name', max_length=1000)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)


class Degree(models.Model):
    """For Education model."""
    degree = models.CharField(primary_key=True, max_length=500)

    def __str__(self):
        return str(self.degree)


class Education(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    degree = models.ForeignKey(Degree, on_delete=models.SET_NULL, null=True)
    discipline = models.CharField(verbose_name='Discipline/Field', max_length=200)
    institute = models.CharField(verbose_name='Institute Name', max_length=1000)
    admission_year = models.IntegerField(null=True)
    passing_year = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.profile.name} - {self.institute}'
