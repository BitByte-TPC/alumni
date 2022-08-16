from django.shortcuts import render
from .models import Job
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
    posts = Job.objects.all().filter(active=True).order_by('-posting_date') 
    total = len(posts) 
    page = request.GET.get('page', 1)
    if posts:
        # using paginator to list 10 jobs at a page
        paginator = Paginator(posts, 10)
        try:
            current_page = paginator.page(page) 
        except PageNotAnInteger:
            current_page = paginator.page(1)
        except EmptyPage:
            current_page = paginator.page(paginator.num_pages)
        if request.user.is_superuser:
            # retrieving jobs of current_page into a list using zip 
            # it will pair job with person
            person_list = [] 
            for i in posts:
                person_list.append(i.person)
            job_list = zip(current_page, person_list)
            return render(request, "jobs/job_home.html", {'job_list': job_list, 'current_page': current_page, 'total': total})
        else:
            person_list = []
            for i in posts:
                person_list.append(i.person)
            job_list = zip(current_page, person_list)
            return render(request, "jobs/job_home.html", {'job_list': job_list, 'current_page': current_page, 'total': total})
    else:
        job_list = []
        return render(request, "jobs/job_home.html", {'job_list': job_list, 'total': total})


@login_required
def filter(request):
    viewname = "filter"
    job_role = request.POST.get('position')
    page = request.GET.get('page', 1)
    type = request.POST.get('type')

    if job_role != 'all' and type != 'all':
        posts = Job.objects.filter(job_role=job_role, type=type, active=True).order_by('-posting_date')
    elif job_role != 'all' and type == 'all':
        posts = Job.objects.filter(job_role=job_role, active=True).order_by('-posting_date')
    elif job_role == 'all' and type != 'all':
        posts = Job.objects.filter(type=type, active=True).order_by('-posting_date')
    else:
        return redirect('jobs:index', permanent=True)

    if posts:
        messages.success(request, "Found " + str(posts.count()) + " posts matching your query!")
        paginator = Paginator(posts, 10)
        try:
            current_page = paginator.page(page)
        except PageNotAnInteger:
            current_page = paginator.page(1)
        except EmptyPage:
            current_page = paginator.page(paginator.num_pages)
        person_list = []
        for i in posts:
            person_list.append(i.person)
            job_list = zip(current_page, person_list)
        return render(request, "jobs/job_home.html", {'job_list': job_list, 'current_page': current_page, 'viewname': viewname})

    else:
        job_list = []
        messages.error(request, "No posts matching your current requirements.")
        return render(request, "jobs/job_home.html", {'job_list': job_list, 'viewname': viewname})


@login_required
def add_opportunity(request):
    if request.method == 'POST':
        try:
            type = request.POST.get('type')
            job_role = request.POST.get('position')
            org_name = request.POST.get('company')
            location = request.POST.get('location')
            raw_link = request.POST.get('link')
            link = raw_link if raw_link.startswith('https://') or raw_link.startswith(
                'http://') else 'https://' + raw_link

            job_desc = request.POST.get('desc')
            stipend = int(request.POST.get('stipend')) if request.POST.get('stipend') else None
            exp_req = int(request.POST.get('exp_req')) if request.POST.get('exp_req') else None
            tenure = int(request.POST.get('tenure')) if request.POST.get('tenure') else None
            last_date = request.POST.get('last_date') if request.POST.get('last_date') else None
            join_date = request.POST.get('join_date') if request.POST.get('join_date') else None
            person = User.objects.get(username=str(request.user))

            insert = Job.objects.create(type=type, job_role=job_role, org_name=org_name, location=location, job_desc=job_desc,
                                        stipend=stipend, exp_req=exp_req, last_date=last_date, join_date=join_date,
                                        tenure=tenure, link=link, posting_date=date.today(), person=person, active=True)
            print(insert)
            messages.success(request, "Job opportunity added successfully!")

        except Exception as e:
            messages.error(request, "Some error occurred, try again.")
            print("Exception while adding new job: ", e)

        return redirect('jobs:index', permanent=True)

    return render(request, "jobs/add_opportunity.html")


@login_required
@user_passes_test(
    is_superuser, redirect_field_name=None,
    login_url=reverse_lazy('home')
)
def delete_job(request, job_id=None):
    if job_id:
        job_post = Job.objects.get(id=job_id)
        job_post.active = False
        job_post.save()
        messages.success(request, "Job opportunity removed successfully!")

    return redirect('jobs:index', permanent=True)
