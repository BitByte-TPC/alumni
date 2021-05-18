from django.db import models

# Create your models here.
class EmailTemplate(models.Model):
    template_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=500)
    body = models.TextField()

    def __str__(self):
        return self.name
