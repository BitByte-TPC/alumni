from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from .models import Profile, Previous_Experience
from datetime import datetime

try:
    from collections.abc import defaultdict
except ImportError:
    from collections import defaultdict


#
# Create your views here.

# @login_required
def profile(request, username):
    user = Profile.objects.get(user__username=username)
    experiences = Previous_Experience.objects.filter(alumni = username)

    user.roll_no = str(user.roll_no)
    user = vars(user)

    temp = list()

    for i in experiences.values():
        temp.append(i)

    user.update({'experiences': temp})

    print(user)
    return render(request, "alumniprofile/profile.html", user)


def index(request):
    years = set(Profile.objects.all().values_list('batch', flat=True))
    print(years)
    return render(request, "alumniprofile/index.html", {'years': years})


def index_year(request, year):
    alumni = Profile.objects.filter(batch=year)
    return render(request, "alumniprofile/index_year.html", {'alumni': alumni})


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
        if not request.user.is_authenticated:
            return render(request, "/")

        user = request.user
        form = editProfile()
        return render(request, "alumniprofile/edit.html", {'form': form, 'user' : user })
'''

def add_experience(request):
    alumni = Profile.objects.get(user__username = request.user)

    if request.method == "POST":
        prev_role = request.POST.get('prev_role')
        prev_branch = request.POST.get('prev_branch')
        prev_organisation = request.POST.get('prev_org')
        start_date = request.POST.get('join_date')
        end_date = request.POST.get('end_date')

        experience = Previous_Experience(alumni = alumni, prev_role = prev_role, prev_branch = prev_branch, prev_organisation = prev_organisation, start_date = start_date, end_date = end_date)
        experience.save()

    return render(request, "alumniprofile/profile.html", vars(alumni))