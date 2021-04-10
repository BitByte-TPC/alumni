from django.db import models


# Create your models here.
class MapPoints(models.Model):
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    lat = models.FloatField()
    long = models.FloatField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (self.city + ": " + str(self.lat) + ", " + str(self.long))
