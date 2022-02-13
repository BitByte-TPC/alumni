from django.shortcuts import render, redirect
from django import forms
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.db.models import Count
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin

from .forms import RegisterForm, ProfileEdit, NewRegister, SignUp
from .token import account_activation_token
from applications.events_news.models import Event, Attendees
from applications.alumniprofile.models import Profile, Constants, Batch
from applications.news.models import News
from applications.gallery.models import Album
from applications.geolocation.views import addPoints
import datetime
from django.utils import timezone
from itertools import chain


# Create your views here.

class LoginFormView(SuccessMessageMixin, LoginView):
    template_name = 'AlumniConnect/login.html'
    redirect_authenticated_user = True
    # success_url = '/'
    success_message = "Logged in successfully!"


def index(request):
    sname = None
    if request.user.is_authenticated:
        sname = request.user.get_short_name()
    now = timezone.now()
    events = Event.objects.filter(start_date__gte=now).order_by('start_date').annotate(
        count=Count('attendees__user_id'))
    events_completed = Event.objects.filter(end_date__lt=now).order_by('-start_date').annotate(
        count=Count('attendees__user_id'))
    # Add Check here
    news = News.objects.filter().order_by('-date')
    # messages.success(request, 'Your password was successfully updated!')
    events_to_display = list(chain(events, events_completed))[:3]
    albums_list = Album.objects.order_by(
        '-created').annotate(images_count=Count('albumimage'))[:3]
    return render(request, "AlumniConnect/index.html",
                  {'name': sname, 'events': events_to_display, 'news': news, 'albums': albums_list})


def alumniBody(request):
    return render(request, "AlumniConnect/alumnibody.html")


def alumniCard(request):
    return render(request, "AlumniConnect/alumnicard.html")


def gallery(request):
    return render(request, "AlumniConnect/gallery.html")


def job_posting(request):
    return render(request, "AlumniConnect/job_posting.html")


# def jobboard(request):
#     return render(request, "env/Lib/site-packages/gallery.html")


def register(request):
    check = False
    l = None
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        print(request.POST)
        if form.is_valid():
            batch = form.cleaned_data.get('batch')
            branch = form.cleaned_data.get('branch')
            programme = form.cleaned_data.get('programme')
            l = Profile.objects.filter(
                batch=batch, programme=programme, branch=branch)
            print('Testing output\n')
            print(l)
            check = True

    else:
        form = RegisterForm()
    return render(request, 'AlumniConnect/registration.html', {'form': form, 'check': check, 'l': l})


def signup(request):
    if request.method == 'POST':
        form = SignUp(request.POST)
        if form.is_valid():

            # CREATING THE USER FROM THE MODEL FORM DATA
            user = form.save(commit=False)
            user.username = form.cleaned_data.get('username')
            user.email = str(form.cleaned_data.get('email'))
            user.is_active = False
            user.save()
            # THEN CREATING THE PROFILE INSTANCE AND SAVING THE USER AND USER_TYPE
            profile = Profile.objects.create(
                roll_no=form.cleaned_data.get('username'),
                email=form.cleaned_data.get('email'),
                user_type=form.cleaned_data.get('user_type'),
                user=user,
                batch=Batch(2009),
            )

            profile.save()
            messages.success(
                request, f'Your account has been created! You are now able to log in')
            return render(request, 'AlumniConnect/confirm_email.html')
            # return HttpResponseRedirect('/')
    else:
        form = SignUp()
    return render(request, 'AlumniConnect/signup.html', {'form': form})


def reg_no_gen(degree_, spec_, year):
    degree = {"B.Tech": "1", "B.Des": '2',
              "M.Tech": '3', "M.Des": '4', "PhD": '5'}
    spec = {"NA": '00', "CSE": "01", "ECE": "02",
            "ME": "03", "MT": "04", "NS": "05", "DS": "06"}
    last_reg_no = Profile.objects.filter(
        year_of_admission=year).order_by('user__date_joined').last()
    # print(last_reg_no)
    new_reg_no = (int(str(last_reg_no.reg_no)[-4:]) + 1) if last_reg_no else 1
    return degree[degree_] + spec[spec_] + str(year)[2:] + str(convert_int(new_reg_no, 4))


def convert_int(number, decimals):
    return str(number).zfill(decimals)


def new_register(request):
    if request.method == 'POST':
        form = NewRegister(request.POST, request.FILES)
        # print (request.POST)
        if form.is_valid():
            try:
                first_name, last_name = request.POST['name'].split(' ', 1)
            except:
                first_name = request.POST['name']
                last_name = ""
            # print (form.cleaned_data.get('date_of_joining'))
            profile = form.save(commit=False)
            profile.reg_no = reg_no_gen(
                profile.programme, profile.branch, profile.year_of_admission)
            profile.country = request.POST['country']
            profile.state = request.POST['state']
            profile.city = request.POST['city']
            password = User.objects.make_random_password(length=10)
            # password = '12345678'
            user = User.objects.create_user(
                username=str(form.cleaned_data.get('roll_no')),
                first_name=first_name,
                last_name=last_name,
                email=str(form.cleaned_data.get('email')),
                password=password,
                is_active=True
            )
            profile.user = user
            profile.save()
            mappt = addPoints({'city': str(request.POST['city']), 'state': str(request.POST['state']),
                               'country': str(request.POST['country'])})
            print('Adding Map Point Status: ' + str(mappt))
            return render(request, 'AlumniConnect/confirm_email.html')
    else:
        form = NewRegister()
    return render(request, 'AlumniConnect/profileedit.html', {'form': form, 'edit': False})


@login_required
def profileedit(request, id):
    if request.user.username == id:
        profile = Profile.objects.get(roll_no=id)
        if request.method == 'POST':
            form = ProfileEdit(request.POST, request.FILES, instance=profile)
            if form.is_valid():
                profile = form.save()
                profile.save()
                return HttpResponseRedirect('/profile/' + id)
        else:
            print("here")
            form = ProfileEdit(instance=profile)
        return render(request, 'AlumniConnect/profileedit.html',
                      {'form': form, 'C': profile.country, 's': profile.state, 'c': profile.city, 'edit': True})
    else:
        return HttpResponseRedirect('/')


def activate(request, uidb64, token):
    print('inside activate')
    try:
        uid = urlsafe_base64_decode(uidb64)
        print(uid)
        u = User.objects.get(username=uid)
        print(u)
    except(TypeError, ValueError, OverflowError):
        u = None
    if u is not None and account_activation_token.check_token(u, token):
        u.is_active = True
        u.save()
        login(request, u)
        # return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
        return HttpResponseRedirect('/password/')
    else:
        return HttpResponse('Activation link is invalid!')
    return redirect('/')


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(
                request, 'Your password was successfully updated!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'AlumniConnect/change_password.html', {'form': form})
