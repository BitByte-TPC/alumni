from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from .models import Constants, Degree, Education, Profile, PastExperience
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
    current_education = Education.objects.filter(profile=profile, passing_year=None).order_by('-admission_year')
    education = Education.objects.filter(profile=profile, passing_year__isnull=False).order_by('-passing_year', '-admission_year')

    profile.roll_no = str(profile.roll_no)
    profile = vars(profile)

    # Add experience
    profile.update({
        'current_experiences': current_experiences,
        'experiences': experiences,
        'EMPLOYMENT_TYPE': Constants.EMPLOYMENT_TYPE,
    })
    
    # Add education
    profile.update({
        'current_education': current_education,
        'education': education,
        'ADMISSION_YEAR': Constants.ADMISSION_YEAR,
        'PASSING_YEAR': Constants.PASSING_YEAR,
        'DEGREE': list(Degree.objects.all().order_by('degree')),
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

        PastExperience.objects.create(
            profile=profile, position=position, emp_type=emp_type,
            organisation=organisation, start_date=start_date,
            end_date=end_date
        )

    return redirect('profile:profile', request.user.username)


def get_education_form_field_names():
    return [
        'edu_degree_select',
        'edu_degree_input',
        'edu_degree_not_listed',
        'edu_discipline',
        'edu_institute',
        'edu_admission_year',
        'edu_passing_year',
        'edu_pursuing'
    ]

def create_new_education(request, profile):
    degree_val = request.POST.get('edu_degree_select')
    if request.POST.get('edu_degree_not_listed'):
        degree_val = request.POST.get('edu_degree_input')

    degree = Degree.objects.filter(degree=degree_val).first()
    if not degree:
        degree = Degree(degree=degree_val)
        degree.save()

    discipline =request.POST.get('edu_discipline')
    institute =request.POST.get('edu_institute')
    admission_year =request.POST.get('edu_admission_year')
    passing_year =request.POST.get('edu_passing_year')
    if request.POST.get('edu_pursuing'):
        passing_year = None

    Education.objects.create(
        profile=profile, degree=degree, discipline=discipline,
        institute=institute, admission_year=admission_year,
        passing_year=passing_year
    )


def add_education(request):
    profile = Profile.objects.get(user=request.user)

    if request.method == "POST":
        create_new_education(request, profile)
    
    return redirect('profile:profile', request.user.username)
