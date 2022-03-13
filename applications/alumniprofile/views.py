from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from .models import Constants, Profile, PastExperience
from datetime import datetime

try:
    from collections.abc import defaultdict
except ImportError:
    from collections import defaultdict


#
# Create your views here.

# @login_required
def profile(request, username):
    profile = Profile.objects.get(user__username=username)
    current_experiences = PastExperience.objects.filter(profile=profile, end_date=None).order_by('-start_date')
    experiences = PastExperience.objects.filter(profile=profile, end_date__isnull=False).order_by('-end_date', '-start_date')

    profile.roll_no = str(profile.roll_no)
    profile = vars(profile)

    profile.update({
        'current_experiences': current_experiences,
        'experiences': experiences,
        'EMPLOYMENT_TYPE': Constants.EMPLOYMENT_TYPE,
    })

    return render(request, "alumniprofile/profile.html", profile)


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
    profile = Profile.objects.get(user=request.user)

    if request.method == "POST":
        position = request.POST.get('position')
        emp_type = request.POST.get('emp_type')
        organisation = request.POST.get('organisation')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date') or None

        PastExperience.objects.create(profile=profile, position=position, emp_type=emp_type, organisation=organisation, start_date=start_date, end_date=end_date)

    return redirect('profile:profile', request.user.username)