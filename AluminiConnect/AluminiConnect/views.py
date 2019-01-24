from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, "AluminiConnect/index.html")

def login_view(request):
    return render(request, "awards/home.html")