from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .models import Profile
# Create your views here.

def index(request, username):
    user = Profile.objects.get(user__username = username)
    print(vars(user))
    return render(request, "alumniprofile/profile.html", vars(user))
