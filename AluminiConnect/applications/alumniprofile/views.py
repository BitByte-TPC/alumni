from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from .models import Profile
from datetime import datetime
from collections import defaultdict 
#
# Create your views here.

@login_required
def profile(request, username):
    user = Profile.objects.get(user__username = username)
    user.roll_no = str(user.roll_no)
    print(vars(user))
    return render(request, "alumniprofile/profile.html", vars(user))

def index(request):
    years = set(Profile.objects.all().values_list('batch', flat=True)) 
    print(years)    
    return render(request, "alumniprofile/index.html", {'years':years})

def index_year(request, year):
    alumni = Profile.objects.filter(batch = year)
    return render(request, "alumniprofile/index_year.html", {'alumni':alumni})

'''
def edit(request):
    
    if request.method == "POST":
        print('processing data')
        form = editProfile(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            Profile.user = request.user
            profile.save()

    else:
        if (not request.user.is_authenticated()):
            return render(request, "/")

        user = request.user
        form = editProfile()
        return render(request, "alumniprofile/edit.html", {'form': form, 'user' : user })
'''
    
