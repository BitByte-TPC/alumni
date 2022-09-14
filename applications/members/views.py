from importlib.metadata import requires
import json     

from django.shortcuts import render, redirect
from django.db.models import Count
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from applications.alumniprofile.models import Profile
from django.contrib import messages


# Create your views here.

def index(request):
    counts = Profile.objects.filter(verify=True).values('batch').order_by('-batch').annotate(count=Count('batch'))
    total = 0

    for batch, count in counts.values_list('batch', 'count'):
        total += count

    data = counts.values_list('batch', 'count')

    context = {
               'data': data,
               'total': total,
               }

    return render(request, "members/index.html",context)


def batch(request, year):

    programmes = Profile.objects.values_list('programme', flat=True).distinct()
    data = {}
    for row in programmes:
        # todo: change mail_sent to verify
        result = Profile.objects.filter(batch=year, programme=row, verify=True).values('branch').annotate(count=Count('branch'))
        data[row] = {}
        for item in result:
            data[row][item['branch']] = item['count']

    return render(request, "members/year.html", {'data': data, 'year': year})


def branch(request, programme, year, branch):
    # todo: change mail_sent to verify
    alumni = Profile.objects.filter(programme=programme, batch=year, branch=branch, verify=True)
    return render(request, "members/branch.html", {'data': alumni, 'batch': year, 'branch': branch})

# def sacbody(request):
#     return redirect('members:alumnibody')

def alumnibody(request):
    return render(request, "members/alumnibody.html")


@login_required
def search(request):
    profiles = Profile.objects.all()
    if len(request.POST) > 1:
        if request.POST['search'] != '':
           key = request.POST['search']
           profiles = profiles.filter(name__icontains=key) | Profile.objects.filter(
           roll_no__icontains=key) | Profile.objects.filter(reg_no__icontains=key)

        if request.POST['batch'] != '':
            batch = request.POST['batch']
            profiles = profiles.filter(batch=batch)
            
        if request.POST['city'] != '':
            city = request.POST['city']
            profiles = profiles.filter(city__icontains=city)

        if request.POST['programme'] != '':
            programme = request.POST['programme']
            profiles = profiles.filter(programme__icontains=programme)

        if request.POST['branch'] != '':
            branch = request.POST['branch']
            profiles = profiles.filter(branch__icontains=branch)

        if request.POST['org'] != '':  
            org = request.POST['org']
            profiles1 = profiles.filter(current_organisation__icontains=org)
            profiles2 = profiles.filter(current_university__icontains=org)
            profiles = profiles1 | profiles2

    profiles = profiles.order_by('name')

    context = {'profiles': profiles,
               'keyy': 1,
               'zero': len(profiles),
               'request': request.POST
               }
    
    if len(profiles):
        messages.success(request,"Total "+str(len(profiles))+" Alumni Found")
    else:
         messages.error(request, "No Result Found ")

        

    return render(request, "members/index.html", context)

def autoSearch(request):
    if request.is_ajax():
        # print(request.POST['term'], request.GET['te'])
        key = request.GET['term']
        search_qs = Profile.objects.filter(name__icontains=key) | Profile.objects.filter(
            roll_no__icontains=key) | Profile.objects.filter(reg_no__icontains=key)
        data = []
        for r in search_qs:
            data.append(r.name)
    else:
        data = 'fail'
    return JsonResponse(data, safe=False)


@login_required
def mapSearch(request):
    key = request.GET['search']
    city = key.split(',', 1)[0]
    profiles = Profile.objects.filter(city__icontains=city)
    profiles = profiles.order_by('name')
    context = {'profiles': profiles,
               'keyy': key,
               'zero': len(profiles),
               'map': True
                }
    return render(request, "members/index.html", context)
