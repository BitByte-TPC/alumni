from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .models import Profile
# Create your views here.

def index(request, username):
    users = Profile.objects.get(user__username = username)
    return render(request, "alumniprofile/profile.html", {"users" : users})
    
=======
    user = Profile.objects.get(user__username = username)
    print(vars(user))
    return render(request, "alumniprofile/profile.html", vars(user))
>>>>>>> 13d6c5c07de04ad55fa7eed61f262045e4469818
