from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .models import Profile
# Create your views here.

def index(request, username):
        #use username as roll number in db
        #small hack to connect User to profile 
        username = '2017180'
        profile = Profile.objects.get( roll_no = username)
        profile.username = username
        print(vars(profile))
        return render(request, 'alumniprofile/profile.html', vars(profile))    
