from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .models import Profile
# Create your views here.

def index(request, username):
<<<<<<< HEAD
    users = Profile.objects.get(user__username = username)
    return render(request, "alumniprofile/profile.html", {"users" : users})
=======
        profile = Profile.objects.get( roll_no = '2017180')
        profile.username = username
        print(vars(profile))
        return render(request, 'alumniprofile/profile.html', vars(profile))    
>>>>>>> 9405bf14dda453968793948f7cacebfc466f1580
