from django.shortcuts import render
from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from .forms import UserRegistrationForm
from applications.events_news.models import Event
import datetime
# Create your views here.

def index(request):
    sname = None
    if( request.user.is_authenticated()):
        sname = request.user.get_short_name()
    events_list = Event.objects.filter().order_by('start_date')[:3]
    #Add Check here
    return render(request, "AluminiConnect/index.html", {'name':sname, 'events':events_list})

def alumniBody(request):
    return render(request, "AluminiConnect/alumnibody.html")

def auth(request):

    print(request.POST.get('submit'))

    if request.POST.get('submit') == 'signup':
        form = UserRegistrationForm(request.POST)
        
        if form.is_valid():
            userObj = form.cleaned_data
            username = userObj['username']
            email = userObj['email']
            pswd = userObj['password']

            if not (User.objects.filter(username = username).exists() or User.objects.filter(email=email).exists()):
                User.objects.create_user(username,email,pswd)
                user = authenticate(username = username, password = pswd)
                login(request,user)
                return HttpResponseRedirect('/')
            else:
                raise forms.ValidationError('Looks like a username with that email or password already exists')

    if request.POST.get('submit') == 'login':
        print('User login')
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            user.last_visit = datetime.datetime.now()
            return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect('/login/')
        
    
    return render(request, 'AluminiConnect/signup.html')
    
def register(request):
    return render(request, 'AluminiConnect/registration.html')