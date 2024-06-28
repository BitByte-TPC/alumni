from django.shortcuts import render
from django.db.models import Q
from .models import Blog
from .forms import BlogSearchForm

def blog_list(request):
    form = BlogSearchForm(request.GET)
    blogs = Blog.objects.all()

    if request.GET:
        username = request.GET.get('username')
        title = request.GET.get('title')
        tags = request.GET.get('tags')
        campaign = request.GET.get('campaign')
        is_self = request.GET.get('is_self')

        if username:
            blogs = blogs.filter(author__username__icontains=username)
        if title:
            blogs = blogs.filter(title__icontains=title)
        if tags:
            blogs = blogs.filter(tags__icontains=tags)
        if campaign:
            blogs = blogs.filter(campaign__icontains=campaign)
        if is_self:
            blogs = blogs.filter(is_self=True)

    return render(request, 'blog/blog_list.html', {'blogs': blogs,'form': form})
