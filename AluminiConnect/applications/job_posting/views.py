from django.shortcuts import render
from .models import Posting
from datetime import date
from django.contrib import messages
from django.shortcuts import redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.urls import reverse_lazy


def is_superuser(user):
    return user.is_superuser


@login_required
def index(request):
    posts = Posting.objects.all().filter(active=True).order_by('-posting_date')
    total = len(posts)
    page = request.GET.get('page', 1)
    if posts:
        paginator = Paginator(posts, 10)
        try:
            ls2 = paginator.page(page)
        except PageNotAnInteger:
            ls2 = paginator.page(1)
        except EmptyPage:
            ls2 = paginator.page(paginator.num_pages)
        if request.user.is_superuser:
            ls = []
            for i in posts:
                ls.append(i.person)
            ls1 = zip(ls2, ls)
            return render(request, "job_posting/home.html", {'ls1': ls1, 'ls2': ls2, 'total': total})
        else:
            ls = []
            for i in posts:
                ls.append(i.person)
            ls1 = zip(ls2, ls)
            return render(request, "job_posting/home.html", {'ls1': ls1, 'ls2': ls2, 'total': total})
    else:
        ls1 = []
        return render(request, "job_posting/home.html", {'ls1': ls1, 'total': total})


@login_required
def filter(request):
    viewname = "filter"
    position = request.POST.get('position')
    page = request.GET.get('page', 1)
    type = request.POST.get('type')

    if position != 'all' and type != 'all':
        posts = Posting.objects.filter(position=position, type=type, active=True).order_by('-posting_date')
    elif position != 'all' and type == 'all':
        posts = Posting.objects.filter(position=position, active=True).order_by('-posting_date')
    elif position == 'all' and type != 'all':
        posts = Posting.objects.filter(type=type, active=True).order_by('-posting_date')
    else:
        return redirect('jobs:index', permanent=True)

    if posts:
        messages.success(request, "Found " + str(posts.count()) + " posts matching your query!")
        paginator = Paginator(posts, 10)
        try:
            ls2 = paginator.page(page)
        except PageNotAnInteger:
            ls2 = paginator.page(1)
        except EmptyPage:
            ls2 = paginator.page(paginator.num_pages)

        ls = []
        for i in posts:
            ls.append(i.person)
            ls1 = zip(ls2, ls)
        return render(request, "job_posting/home.html", {'ls1': ls1, 'ls2': ls2, 'viewname': viewname})

    else:
        ls1 = []
        messages.error(request, "No posts matching your current requirements.")
        return render(request, "job_posting/home.html", {'ls1': ls1, 'viewname': viewname})


@login_required
def post(request):
    if request.method == 'POST':
        try:
            type = request.POST.get('type')
            position = request.POST.get('position')
            company = request.POST.get('company')
            location = request.POST.get('location')
            raw_link = request.POST.get('link')
            link = raw_link if raw_link.startswith('https://') or raw_link.startswith(
                'http://') else 'https://' + raw_link

            desc = request.POST.get('desc')
            stipend = int(request.POST.get('stipend')) if request.POST.get('stipend') else None
            exp_req = int(request.POST.get('exp_req')) if request.POST.get('exp_req') else None
            tenure = int(request.POST.get('tenure')) if request.POST.get('tenure') else None
            last_date = request.POST.get('last_date') if request.POST.get('last_date') else None
            join_date = request.POST.get('join_date') if request.POST.get('join_date') else None
            person = User.objects.get(username=str(request.user))

            insert = Posting.objects.create(type=type, position=position, company=company, location=location, desc=desc,
                                            stipend=stipend, exp_req=exp_req, last_date=last_date, join_date=join_date,
                                            tenure=tenure, link=link, posting_date=date.today(),
                                            person=person, active=True)
            messages.success(request, "Job opportunity added successfully!")

        except Exception as e:
            messages.error(request, "Some error occurred, try again.")
            print("Exception while adding new job: ", e)

        return redirect('jobs:index', permanent=True)

    return render(request, "job_posting/post.html")


@login_required
@user_passes_test(
    is_superuser, redirect_field_name=None,
    login_url=reverse_lazy('home')
)
def del1(request, i_id=None):
    if i_id:
        job_post = Posting.objects.get(id=i_id)
        job_post.active = False
        job_post.save()
        messages.success(request, "Job opportunity removed successfully!")

    return redirect('jobs:index', permanent=True)
