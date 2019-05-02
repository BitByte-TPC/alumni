from django.shortcuts import render
from django.db.models import Count
# import json as simplejson
from django.core import serializers
# from rest_framework import serializers
from applications.alumniprofile.models import Profile

# Create your views here.
def index(request):
    city = Profile.objects.only('city')
    data = serializers.serialize('json', city,fields=('city'))
    print(data)
    return render(request, "geolocation/index.html",{'city':data})