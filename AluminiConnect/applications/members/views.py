from django.shortcuts import render
from django.db.models import Count
from applications.alumniprofile.models import Profile
# Create your views here.

def index(request):
    counts = Profile.objects.values('batch').order_by('-batch').annotate(count = Count('batch'))
    print(counts)
    return render(request, "members/index.html", {'data' : counts.values_list('batch', 'count')})

def batch(request, year):
    programmes = Profile.objects.values_list('programme', flat=True).distinct()
    data = {}
    for row in programmes:
        result = Profile.objects.filter(batch = year,programme = row,user__is_active=True).values('branch').annotate(count = Count('branch'))
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