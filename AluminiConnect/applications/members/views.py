from django.shortcuts import render
from django.db.models import Count,Q
from django.contrib.auth.models import User
from applications.alumniprofile.models import Profile
# Create your views here.

def index(request):
    counts = Profile.objects.values('batch').order_by('-batch').annotate(count = Count('batch'))
    print(len(counts))
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
    
    print(data) #prints {'B.Des': {'CSE': 1}, 'B.Tech': {'CSE': 1, 'ME': 1}} 
    return render(request, "members/year.html", {'data' : data, 'year': year})

def branch(request, programme, year, branch):
    alumni = Profile.objects.filter(programme = programme, batch = year, branch = branch)
    print(alumni)
    return render(request, "members/branch.html", {'data':alumni, 'batch':year, 'branch':branch})

def sacbody(request):
    return render(request, "members/sacbody.html")

def search(request):
    key = request.GET['search']
    fil = request.GET['filter']
    if fil == 'Name':
        profiles = Profile.objects.filter(name__icontains = key).order_by("name")
    elif fil == 'City':
        profiles = Profile.objects.filter(city__icontains = key).order_by("name")
    elif fil == 'Branch':
        profiles = Profile.objects.filter(branch__icontains = key).order_by("name")
    elif fil == 'Roll_no':
        profiles = Profile.objects.filter(roll_no__icontains = key).order_by("name")
    elif fil == 'Organisation':
        profiles = Profile.objects.filter(current_organisation__icontains = key).order_by("name")    
    context = { 'profiles':profiles,
                'keyy':key,
                'filter' : fil,
                'zero' : len(profiles),
                }
    return render(request,"members/index.html",context)