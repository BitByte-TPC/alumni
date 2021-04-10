from django.shortcuts import render
from .models import Posting
from applications.alumniprofile.models import Profile
from datetime import date
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



# Create your views here.
def index(request):
    posts = Posting.objects.all().order_by('-posting_date')
    page = request.GET.get('page', 1)
    alumni = []
    if posts:
        paginator = Paginator(posts, 5)
        try:
            ls2 = paginator.page(page)
        except PageNotAnInteger:
            ls2 = paginator.page(1)
        except EmptyPage:
            ls2 = paginator.page(paginator.num_pages)
        if request.user.is_superuser:
            ls = []
            for i in posts:
                p = Profile.objects.get(name=i.person)
                ls.append(p.roll_no)
            ls1 = zip(ls2, ls)
            return render(request, "job_posting/home.html", {'ls1': ls1, 'ls2': ls2})
        else:
            alumni = Profile.objects.get(roll_no=str(request.user))
            ls = []
            for i in posts:
                p = Profile.objects.get(name=i.person)
                ls.append(p.roll_no)
            ls1 = zip(ls2, ls)
            return render(request, "job_posting/home.html", {'ls1': ls1, 'alumni': alumni, 'ls2': ls2})
    else:
        ls1 = []
        return render(request, "job_posting/home.html", {'ls1': ls1, 'alumni': alumni})


def filter(request):
    position = request.POST.get('position')
    page = request.GET.get('page', 1)
    type = request.POST.get('type')
    if position and not type:
        posts = Posting.objects.filter(position=position).order_by('-posting_date')
        print(posts)
    elif type and not position:
        posts = Posting.objects.filter(Q(type=type) | Q(type='Both')).order_by('-posting_date')
        print(posts)
    else:
        if type == 'Both':
            posts = Posting.objects.filter(position=position).order_by('-posting_date')
        else:
            posts = Posting.objects.filter(Q(position=position) & Q(type=type)).order_by('-posting_date')
        print(posts)
    if posts:
        paginator = Paginator(posts, 5)
        try:
            ls2 = paginator.page(page)
        except PageNotAnInteger:
            ls2 = paginator.page(1)
        except EmptyPage:
            ls2 = paginator.page(paginator.num_pages)
        if request.user.is_superuser:
            ls = []
            for i in posts:
                p = Profile.objects.get(name=i.person)
                ls.append(p.roll_no)
            ls1 = zip(ls2, ls)
            return render(request, "job_posting/filter.html", {'ls1': ls1, 'ls2': ls2})
        else:
            ls = []
            for i in posts:
                p = Profile.objects.get(name=i.person)
                ls.append(p.roll_no)
            ls1 = zip(ls2, ls)
            alumni = Profile.objects.get(roll_no=str(request.user))
            return render(request, "job_posting/filter.html", {'ls1': ls1, 'alumni': alumni, 'ls2': ls2})
    else:
        ls1 = []
        return render(request, "job_posting/filter.html", {'ls1': ls1})


def new_post(request):
    if request.method == 'POST':
        job_t = request.POST.get('position')
        job_d = request.POST.get('duration')
        desc = request.POST.get('desc')
        link = request.POST.get('link')
        city = request.POST.get('city')
        person = Profile.objects.get(roll_no=str(request.user))
        insert = Posting.objects.create(position=job_t, type=job_d, desc=desc, link=link, posting_date=date.today(),
                                        location=city, person=person)
    return redirect('jobs:index', permanent=True)


def del1(request, i_id=None):
    object = Posting.objects.get(id=i_id)
    object.delete()
    return redirect('jobs:index', permanent=True)
