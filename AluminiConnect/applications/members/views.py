import json

from django.shortcuts import render
from django.db.models import Count,Q
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from applications.alumniprofile.models import Profile

# Create your views here.

def index(request):
    counts = Profile.objects.values('batch').order_by('-batch').annotate(count = Count('batch'))
    # print(len(counts))
    total=0
    for batch,count in counts.values_list('batch', 'count'):
        total+=count
    return render(request, "members/index.html", {'data' : counts.values_list('batch', 'count'), 'total': total})

def batch(request, year):
    programmes = Profile.objects.values_list('programme', flat=True).distinct()
    data = {}
    for row in programmes:
        result = Profile.objects.filter(batch = year,programme = row).values('branch').annotate(count = Count('branch'))
        data[row] = {}
        for item in result:
            data[row][item['branch']] = item['count']
    
    # print(data) #prints {'B.Des': {'CSE': 1}, 'B.Tech': {'CSE': 1, 'ME': 1}} 
    return render(request, "members/year.html", {'data' : data, 'year': year})

def branch(request, programme, year, branch):
    alumni = Profile.objects.filter(programme = programme, batch = year, branch = branch)
    # print(alumni)
    return render(request, "members/branch.html", {'data':alumni, 'batch':year, 'branch':branch})

def sacbody(request):
    return render(request, "members/sacbody.html")

@login_required
def search(request):
    key = request.GET['search']
    profiles = Profile.objects.filter(name__icontains = key) | Profile.objects.filter(roll_no__icontains = key) | Profile.objects.filter(reg_no__icontains = key)
    if len(request.GET) > 1:
        if request.GET['batch'] != '':
            batch = request.GET['batch']
            print(batch)
            profiles = profiles.filter(batch = batch)
            print(profiles)
        if request.GET['city'] != '':
            city = request.GET['city']
            profiles = profiles.filter(city__icontains = city)
        if request.GET['programme'] != 'Programme':
            programme = request.GET['programme']
            profiles = profiles.filter(programme__icontains = programme)
        if request.GET['branch'] != '':
            branch = request.GET['branch']
            profiles = profiles.filter(branch__icontains = branch)
        if request.GET['org'] != '':
            org = request.GET['org']
            profiles1 = profiles.filter(current_organisation__icontains = org)
            profiles2 = profiles.filter(current_university__icontains = org)
            profiles = profiles1 | profiles2
    profiles = profiles.order_by('name')
    context = { 'profiles':profiles,
                'keyy':key,
                'zero' : len(profiles),
                'request' : request.GET
                }
    return render(request,"members/index.html",context)

def autoSearch(request):
    if request.is_ajax():
        key = request.GET['term']
        search_qs = Profile.objects.filter(name__icontains = key) | Profile.objects.filter(roll_no__icontains = key) | Profile.objects.filter(reg_no__icontains = key)
        data = []
        for r in search_qs:
            print(r.name)
            data.append(r.name)
    else:
        data = 'fail'
    return JsonResponse(data,safe = False)

@login_required
def mapSearch(request):
    key = request.GET['search']
    city = key.split(',',1)[0]
    profiles = Profile.objects.filter(city__icontains = city)
    profiles = profiles.order_by('name')
    context = { 'profiles':profiles,
                'keyy':key,
                'zero' : len(profiles),
                'map': True
                }
    return render(request,"members/index.html",context)