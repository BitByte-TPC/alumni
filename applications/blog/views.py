from django.shortcuts import render
from .models import Blog


# Create your views here.

def index(request):
    blog_list = Blog.objects.filter().order_by('-date')
    return render(request, "blog/home.html", {'blog': blog_list})

def blog(request, id):
    n = Blog.objects.get(blog_id=id)
    print("sassa", n)
    return render(request, "blog/blog.html", vars(n))
