from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
# Create your views here.

def index(request, username):
        print(username)
        return render(request, 'alumniprofile/profile.html', {'username' : username})    
