from django.db import models

# Create your models here.
class EmailTemplate(models.Model):
    template_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=500)
    body = models.TextField()

    def __str__(self):
        return self.name


class EmailHistory(models.Model):
    email_template = models.CharField(max_length=100)
    programme = models.CharField(max_length=250)
    batch = models.CharField(max_length=250)
    branch = models.CharField(max_length=250)
    timestamp = models.DateTimeField(auto_now_add=True)
    total_recipients = models.IntegerField()
    total_delivered = models.IntegerField()

    def __str__(self):
        return self.email_template

