from django.shortcuts import render, redirect
from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

from .forms import UserRegistrationForm, RegisterForm1, ProfileEdit
from .token import account_activation_token
from applications.events_news.models import Event
from applications.alumniprofile.models import Profile, Constants
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

def gallery(request):
    return render(request, "AluminiConnect/gallery.html")

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
        l = Profile.objects.get(user = user)
        print(l)
        if l.is_registered:
            if user is not None:
                login(request,user)
                user.last_visit = datetime.datetime.now()
                return HttpResponseRedirect('/')
            else:
                return HttpResponseRedirect('/login/')
        
    
    return render(request, 'AluminiConnect/signup.html')
    
def register1(request):
    check=False
    l = None
    if request.method == 'POST':
        form = RegisterForm1(request.POST)
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
        form = RegisterForm1()
    return render(request, 'AluminiConnect/registration.html', {'form': form, 'check': check, 'l': l})

def profileedit(request, id):
    l = Profile.objects.get(roll_no = id)

    print(l)
    if request.method == 'POST':
        form = ProfileEdit(request.POST, instance = l)
        print (request.POST)
        if form.is_valid():
            l =form.save(commit=False)
            l.save()
            if not l.is_registered:
                current_site = get_current_site(request)
                mail_subject = 'Activate your Alumni Account'
                message = render_to_string('AluminiConnect/acc_active_email.html', {
                    'user' : l.roll_no,
                    'domain' : current_site.domain,
                    'uid' : urlsafe_base64_encode(force_bytes(l.roll_no )).decode(),
                    'token' : account_activation_token.make_token(l.user),
                })
                print ('printinemail\n')
                print (l.user.email)
                to_email = l.user.email
                email = EmailMessage( mail_subject, message, to=[to_email] )
                email.send()
                #return HttpResponse('Please confirm your email address to complete registeration process..')
                return HttpResponseRedirect('/confirm/')
    else:
        form = ProfileEdit(instance = l)
    return render(request, 'AluminiConnect/profileedit.html', {'form' :form, 'l': l})

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