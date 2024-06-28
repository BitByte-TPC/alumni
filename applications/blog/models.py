from django.db import models
from django.contrib.auth.models import User


class Blog(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    tags = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    campaign = models.CharField(max_length=200, blank=True, null=True)
    is_self = models.BooleanField(default=False)
    content = models.TextField()

    def __str__(self):
        return self.title
