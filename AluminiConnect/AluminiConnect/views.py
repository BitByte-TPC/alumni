from django.shortcuts import render
from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from .forms import UserRegistrationForm
# Create your views here.

def index(request):
    return render(request, "AluminiConnect/index.html")

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

        user = authenticate(username=username, password=password, request=request)
        login(request,user)
        return HttpResponseRedirect('/')
    
    return render(request, 'AluminiConnect/signup.html')
    
            
def login_view(request):
    return render(request, "awards/home.html")
