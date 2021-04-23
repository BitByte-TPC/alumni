from django.shortcuts import render
from .models import Posting
from applications.alumniprofile.models import Profile
from datetime import date
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages 
from django.shortcuts import redirect
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.
def index(request):
    posts = Posting.objects.all().order_by('-posting_date')
    page = request.GET.get('page', 1)
    if posts:
        paginator = Paginator(posts, 6)
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
            ls = []
            for i in posts:
                p = Profile.objects.get(name=i.person)
                ls.append(p.roll_no)
            ls1 = zip(ls2, ls)
            return render(request, "job_posting/home.html", {'ls1': ls1, 'ls2': ls2})
    else:
        ls1 = []
        return render(request, "job_posting/home.html", {'ls1': ls1})


def filter(request):
    viewname = "filter";
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
        messages.success(request, "Found " + str(posts.count()) + " posts matching your query!")
        paginator = Paginator(posts, 6)
        try:
            ls2 = paginator.page(page)
        except PageNotAnInteger:
            ls2 = paginator.page(1)
        except EmptyPage:
            ls2 = paginator.page(paginator.num_pages)

        ls = []
        for i in posts:
            p = Profile.objects.get(name=i.person)
            ls.append(p.roll_no)
            ls1 = zip(ls2, ls)
            return render(request, "job_posting/home.html", {'ls1': ls1, 'ls2': ls2, 'viewname': viewname})
    else:
        ls1 = []
        messages.error(request, "No posts matching your current requirements.")
        return render(request, "job_posting/home.html", {'ls1': ls1, 'viewname': viewname})

def post(request):
    return render(request, "job_posting/post.html")

def new_post(request):
    if request.method == 'POST':
        try:
            type = request.POST.get('type')
            position = request.POST.get('position')
            company = request.POST.get('company')
            location = request.POST.get('location')
            desc = request.POST.get('desc')
            stipend = request.POST.get('stipend')
            exp_req = request.POST.get('exp_req')
            last_date = request.POST.get('last_date')
            join_date = request.POST.get('join_date')
            tenure = request.POST.get('tenure')
            link = request.POST.get('link')
            person = Profile.objects.get(roll_no=str(request.user))
            insert = Posting.objects.create(type=type, position=position, company=company, location=location, desc=desc, stipend=stipend, exp_req=exp_req, last_date=last_date, join_date=join_date, tenure=tenure, link=link, posting_date=date.today(),
                person=person)
            messages.success(request, "Job posted successfully!")
        except Exception:
            messages.error(request, "Some error occurred, try again.")
            
    return redirect('jobs:index', permanent=True)


def del1(request, i_id=None):
    object = Posting.objects.get(id=i_id)
    object.delete()
    return redirect('jobs:index', permanent=True)
