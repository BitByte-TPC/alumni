from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .models import Profile
# Create your views here.

def index(request, username):
        profile = Profile.objects.get( roll_no = '2017180')
        profile.username = username
        print(vars(profile))
        return render(request, 'alumniprofile/profile.html', vars(profile))    
