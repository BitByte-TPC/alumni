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
    #messages.success(request, 'Your password was successfully updated!')
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
        #print (request.POST)
        if form.is_valid():
            try:
                first_name,last_name=request.POST['name'].split(' ',1)
            except:
                first_name=request.POST['name']
                last_name=""
            #print (form.cleaned_data.get('date_of_joining'))
            profile = form.save(commit=False)
            profile.reg_no = reg_no_gen(profile.programme, profile.branch, profile.year_of_admission)
            profile.country=request.POST['country']
            profile.state=request.POST['state']
            profile.city=request.POST['city']
            user = User.objects.create_user(
                username=str(form.cleaned_data.get('roll_no')),
                first_name=first_name,
                last_name=last_name,
                email=str(form.cleaned_data.get('email')),
                password=profile.reg_no,
                is_active = True
                )
            profile.user = user
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

from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template import loader
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from settings import DEFAULT_FROM_EMAIL
from django.views.generic import *
from utils.forms.reset_password_form import PasswordResetRequestForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models.query_utils import Q

class ResetPasswordRequestView(FormView):
    template_name = "registration/password_reset_form.html"    #code for template is given below the view's code
    success_url = '/account/login'
    form_class = PasswordResetRequestForm

    @staticmethod
    def validate_email_address(email):
    '''
    This method here validates the if the input is an email address or not. Its return type is boolean, True if the input is a email address or False if its not.
    '''
        try:
            validate_email(email)
            return True
        except ValidationError:
            return False

    def post(self, request, *args, **kwargs):
    '''
    A normal post request which takes input from field "email_or_username" (in ResetPasswordRequestForm).
    '''
        form = self.form_class(request.POST)
        if form.is_valid():
            email= form.cleaned_data["email"]
            roll = form.cleaned_data["roll_no"]
        if self.validate_email_address(email) is True:                 #uses the method written above
            '''
            If the input is an valid email address, then the following code will lookup for users associated with that email address. If found then an email will be sent to the address, else an error message will be printed on the screen.
            '''
            associated_users= User.objects.filter(username=roll_no, email=email)
            if associated_users.exists():
                for user in associated_users:
                        c = {
                            'email': user.email,
                            'domain': request.META['HTTP_HOST'],
                            'site_name': 'your site',
                            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                            'user': user,
                            'token': default_token_generator.make_token(user),
                            'protocol': 'http',
                            }
                        subject_template_name='registration/password_reset_subject.txt'
                        # copied from django/contrib/admin/templates/registration/password_reset_subject.txt to templates directory
                        email_template_name='registration/password_reset_email.html'
                        # copied from django/contrib/admin/templates/registration/password_reset_email.html to templates directory
                        subject = loader.render_to_string(subject_template_name, c)
                        # Email subject *must not* contain newlines
                        subject = ''.join(subject.splitlines())
                        email = loader.render_to_string(email_template_name, c)
                        send_mail(subject, email, DEFAULT_FROM_EMAIL , [user.email], fail_silently=False)
                result = self.form_valid(form)
                messages.success(request, 'An email has been sent to ' + data +". Please check its inbox to continue reseting password.")
                return result
            result = self.form_invalid(form)
            messages.error(request, 'No user is associated with this email address')
            return result
        else:
            '''
            If the input is an username, then the following code will lookup for users associated with that user. If found then an email will be sent to the user's address, else an error message will be printed on the screen.
            '''
            associated_users= User.objects.filter(username=data)
            if associated_users.exists():
                for user in associated_users:
                    c = {
                        'email': user.email,
                        'domain': 'example.com', #or your domain
                        'site_name': 'example',
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'user': user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                        }
                    subject_template_name='registration/password_reset_subject.txt'
                    email_template_name='registration/password_reset_email.html'
                    subject = loader.render_to_string(subject_template_name, c)
                    # Email subject *must not* contain newlines
                    subject = ''.join(subject.splitlines())
                    email = loader.render_to_string(email_template_name, c)
                    send_mail(subject, email, DEFAULT_FROM_EMAIL , [user.email], fail_silently=False)
                result = self.form_valid(form)
                messages.success(request, 'Email has been sent to ' + data +"'s email address. Please check its inbox to continue reseting password.")
                return result
            result = self.form_invalid(form)
            messages.error(request, 'This username does not exist in the system.')
            return result
        messages.error(request, 'Invalid Input')
        return self.form_invalid(form)