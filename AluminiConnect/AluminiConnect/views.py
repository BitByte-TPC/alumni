from django.shortcuts import render, redirect
from django import forms
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

from .forms import UserRegistrationForm, RegisterForm, ProfileEdit, NewRegister
from .token import account_activation_token
from applications.events_news.models import Event
from applications.alumniprofile.models import Profile, Constants
from applications.news.models import News
import datetime
from django.utils import timezone
from itertools import chain
# Create your views here.

def index(request):
    sname = None
    if( request.user.is_authenticated()):
        sname = request.user.get_short_name()
    now = timezone.now()
    events = Event.objects.filter(start_date__gte=now).order_by('start_date')
    events_completed = Event.objects.filter(end_date__lt=now).order_by('-start_date')
    #Add Check here
    news = News.objects.filter().order_by('-date')
    return render(request, "AluminiConnect/index.html", {'name':sname, 'events':list(chain(events, events_completed))[:3], 'news': news})

def alumniBody(request):
    return render(request, "AluminiConnect/alumnibody.html")

def gallery(request):
    return render(request, "AluminiConnect/gallery.html")
    
def register(request):
    check=False
    l = None
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        print (request.POST)
        if form.is_valid():
            batch = form.cleaned_data.get('batch')
            branch = form.cleaned_data.get('branch')
            programme = form.cleaned_data.get('programme')
            l = Profile.objects.filter(batch = batch, programme = programme, branch = branch, is_registered = False )
            print ('Testing output\n')
            print (l)
            check = True
            
    else:
        form = RegisterForm()
    return render(request, 'AluminiConnect/registration.html', {'form': form, 'check': check, 'l': l})

def new_register(request):
    if request.method == 'POST':
        form = NewRegister(request.POST)
        print (request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            user = User.objects.create_user(
                username=str(form.cleaned_data.get('roll_no')),
                email=str(form.cleaned_data.get('email')),
                password=str(form.cleaned_data.get('roll_no'))
                )
            profile.user = user
            profile.save()
            if not profile.is_registered:
                current_site = get_current_site(request)
                mail_subject = 'Activate your Alumni Account'
                message = render_to_string('AluminiConnect/acc_active_email.html', {
                    'user' : profile.roll_no,
                    'domain' : current_site.domain,
                    'uid' : urlsafe_base64_encode(force_bytes(profile.roll_no )).decode(),
                    'token' : account_activation_token.make_token(profile.user),
                })
                print ('printing email\n')
                print (profile.user.email)
                to_email = profile.user.email
                email = EmailMessage( mail_subject, message, to=[to_email] )
                email.send()
                #return HttpResponse('Please confirm your email address to complete registeration process..')
                return HttpResponseRedirect('/confirm/')
    else:
        form = NewRegister()
    return render(request, 'AluminiConnect/profileedit.html', {'form' :form, 'edit' : False})

def profileedit(request, id):
    l = Profile.objects.get(roll_no = id)

    print(l)
    if request.method == 'POST':
        form = ProfileEdit(request.POST, instance = l)
        print (request.POST)
        print (form.is_valid(), form.errors, type(form.errors))
        if form.is_valid():
            print(l)
            l =form.save(commit=False)
            print(l.save())
            if not l.is_registered:
                current_site = get_current_site(request)
                mail_subject = 'Activate your Alumni Account'
                message = render_to_string('AluminiConnect/acc_active_email.html', {
                    'user' : l.roll_no,
                    'domain' : current_site.domain,
                    'uid' : urlsafe_base64_encode(force_bytes(l.roll_no )).decode(),
                    'token' : account_activation_token.make_token(l.user),
                })
                print ('printing email\n')
                print (l.user.email)
                to_email = l.user.email
                email = EmailMessage( mail_subject, message, to=[to_email] )
                email.send()
                #return HttpResponse('Please confirm your email address to complete registeration process..')
                return HttpResponseRedirect('/confirm/')
    else:
        print("here")
        form = ProfileEdit(instance = l)
    return render(request, 'AluminiConnect/profileedit.html', {'form' :form, 'l': l, 'edit' : False})

def activate(request, uidb64, token):
    print('inside activate')
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        print(uid)
        user = Profile.objects.get(roll_no = int(uid))
        print(user)
    except(TypeError, ValueError, OverflowError):
        user = None
    if user is not None and account_activation_token.check_token(user.user, token):
        user.is_registered = True
        user.save()
        #return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
        return HttpResponseRedirect('/success/')
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
            messages.success(request, 'Your password was successfully updated!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'AluminiConnect/change_password.html', {'form': form })