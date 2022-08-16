from django.shortcuts import render
from .models import News


# Create your views here.

def index(request):
    news_list = News.objects.filter().order_by('-date')
    return render(request, "news/index.html", {'news': news_list})


def news(request, id):
    n = News.objects.get(news_id=id)
    print("sassa", n)
    return render(request, "news/news.html", vars(n))
