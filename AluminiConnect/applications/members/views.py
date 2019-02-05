from django.shortcuts import render
from django.db.models import Count
from applications.alumniprofile.models import Profile
# Create your views here.

def index(request):
    counts = Profile.objects.values('batch').order_by('-batch').annotate(count = Count('batch'))
    return render(request, "members/index.html", {'data' : counts.values_list('batch', 'count')})

def batch(request, year):
    cse = Profile.objects.filter(batch = year, branch="CSE")# .values_list('programme', flat=True).distinct()
    ece = Profile.objects.filter(batch = year, branch = "ECE")
    me = Profile.objects.filter(batch = year, branch = "ME")
    # #query = {}
    # for row in programmes:
    #     result = Profile.objects.filter(batch = year,programme = row).values_list('branch').annotate(count = Count('branch'))
    #     row = row.replace('.','')
    #     query[row] = {}
    #     for branch, count in result:
    #         query[row][branch] = count
    
    # print(query) #prints {'B.Des': {'CSE': 1}, 'B.Tech': {'CSE': 1, 'ME': 1}} 
    # print(users)
    print(cse)
    return render(request, "members/year.html", {'cse' : cse, 'ece':ece, 'me':me })

def branch(request, year, branch):
    alumni = Profile.objects.filter(batch = year, branch = branch)
    print(alumni)
    return render(request, "members/branch.html", {'a':alumni})
