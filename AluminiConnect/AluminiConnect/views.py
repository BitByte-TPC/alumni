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

def alumniCard(request):
    return render(request, "AluminiConnect/alumnicard.html")

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
            l = Profile.objects.filter(batch = batch, programme = programme, branch = branch)
            print ('Testing output\n')
            print (l)
            check = True
            
    else:
        form = RegisterForm()
    return render(request, 'AluminiConnect/registration.html', {'form': form, 'check': check, 'l': l})

def reg_no_gen(degree_, spec_, year):
    degree = {"B.Tech" : "1", "B.Des" : '2', "M.Tech" : '3', "M.Des" : '4', "PhD" : '5'}
    spec = {"NA" : '00', "CSE": "01", "ECE": "02", "ME":"03", "MT": "04", "NS":"05", "DS":"06"}
    last_reg_no = Profile.objects.filter(year_of_admission=year).order_by('user__date_joined').last()
    #print(last_reg_no)
    new_reg_no = (int(str(last_reg_no.reg_no)[-4:]) + 1) if last_reg_no else 1
    return degree[degree_] + spec[spec_] + str(year)[2:] + str(convert_int(new_reg_no, 4))

def convert_int(number,decimals) :
    return str(number).zfill(decimals)

def new_register(request):
    if request.method == 'POST':
        form = NewRegister(request.POST,request.FILES)
        print (request.POST)
        if form.is_valid():
            try:
                first_name,last_name=request.POST['name'].split(' ',1)
            except:
                first_name=request.POST['name']
                last_name=""
            print (form.cleaned_data.get('date_of_joining'))
            profile = form.save(commit=False)
            user = User.objects.create_user(
                username=str(form.cleaned_data.get('roll_no')),
                first_name=first_name,
                last_name=last_name,
                email=str(form.cleaned_data.get('email')),
                password=str(form.cleaned_data.get('roll_no')),
                is_active = False
                )
            profile.user = user
            profile.reg_no = reg_no_gen(profile.programme, profile.branch, profile.year_of_admission)
            profile.country=request.POST['country']
            profile.state=request.POST['state']
            profile.city=request.POST['city']
            profile.save()
            return render(request, 'AluminiConnect/confirm_email.html')
    else:
        form = NewRegister()
    return render(request, 'AluminiConnect/profileedit.html', {'form' :form, 'edit' : False})

@login_required
def profileedit(request, id):
    if (request.user.username == id):
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
                    return HttpResponseRedirect('/confirm/')
        else:
            print("here")
            form = ProfileEdit(instance = l)
        return render(request, 'AluminiConnect/profileedit.html', {'form' :form, 'l': l, 'edit' : False})
    else:
        return HttpResponseRedirect('/')

def activate(request, uidb64, token):
    print('inside activate')
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        print(uid)
        u = User.objects.get(username = uid)
        print(u)
    except(TypeError, ValueError, OverflowError):
        u = None
    if u is not None and account_activation_token.check_token(u, token):
        u.is_active = True
        u.save() 
        login(request, u)
        #return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
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
            messages.success(request, 'Your password was successfully updated!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'AluminiConnect/change_password.html', {'form': form })
