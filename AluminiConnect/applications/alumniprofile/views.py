from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .models import Profile
# Create your views here.

def index(request, username):
    user = Profile.objects.get(user__username = username)
    user.name = user.user.get_full_name()
    user.sname = user.user.get_short_name()
    user.email = user.user.email
    return render(request, "alumniprofile/profile.html", vars(user))
