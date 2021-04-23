from django.db import models
from applications.alumniprofile.models import Profile


# Create your models here.
class Posting(models.Model):
    position = models.CharField(max_length=20, null=False)
    company = models.CharField(max_length=25, null=False)
    type = models.CharField(max_length=20)
    stipend = models.IntegerField(null=True, blank=True)
    exp_req = models.IntegerField(null=True, blank=True)
    last_date = models.DateField(null=False)
    join_date = models.DateField(null=False)
    tenure = models.IntegerField(null=True, blank=True)
    desc = models.CharField(max_length=300, help_text="Brief Description of job profile", null=True, blank=True)
    link = models.URLField(max_length=300)
    person = models.ForeignKey(Profile, related_name='profile', on_delete=models.CASCADE)
    posting_date = models.DateField()
    location = models.CharField(max_length=30, null=False)

    def __str__(self):
        return self.position + " by " + self.company