from django.shortcuts import render, redirect 
from .models import News


# Create your views here.

def index(request):
    news_list = News.objects.filter().order_by('-date')
    return render(request, "news/index.html", {'news': news_list})


def news(request, id):
    try:
        n = News.objects.get(news_id=id)
        return render(request, "news/news.html", vars(n))
    except News.DoesNotExist:
        return redirect('news:index')