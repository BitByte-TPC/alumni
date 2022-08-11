from django.db import models
from django.contrib.auth.models import User

#Opportunity
class Job(models.Model):
    job_role = models.CharField(max_length=20, null=False) #job role
    org_name = models.CharField(max_length=25, null=False) #org_name
    type = models.CharField(max_length=20)
    link = models.URLField(max_length=1000)
    stipend = models.IntegerField(null=True, blank=True)
    exp_req = models.IntegerField(null=True, blank=True)
    tenure = models.IntegerField(null=True, blank=True)
    last_date = models.DateField(null=True, blank=True)
    join_date = models.DateField(null=True, blank=True)
    job_desc = models.CharField(max_length=300, help_text="Brief Description of job profile", null=True, blank=True)#job_desc
    person = models.ForeignKey(User, on_delete=models.CASCADE)#added_by
    posting_date = models.DateField()
    location = models.CharField(max_length=30, null=False)
    active = models.BooleanField(null=False, default=True)

    def __str__(self):
        return self.job_role + " at " + self.org_name #job_role at org_name
