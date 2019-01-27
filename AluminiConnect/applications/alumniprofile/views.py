from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .models import Profile
# Create your views here.

def index(request, username):
    users = Profile.objects.get(user__username = username)
    return render(request, "alumniprofile/profile.html", {"users" : users})
    