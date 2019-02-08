from django.shortcuts import render
from django.db.models import Count
from applications.alumniprofile.models import Profile
# Create your views here.

def index(request):
    counts = Profile.objects.values('batch').order_by('-batch').annotate(count = Count('batch'))
    print(counts)
    return render(request, "members/index.html", {'data' : counts.values_list('batch', 'count')})

def batch(request, year):
    # users = Profile.objects.values('programme').annotate(count = Count('branch'))
    # print(users)
    programmes = Profile.objects.values_list('programme', flat=True).distinct()
    query = {}
    print(programmes)
    for row in programmes:
        print(type(row))
        result = Profile.objects.filter(batch = year,programme = row).annotate(count = Count('branch')).values_list()
        #row = row.replace('.','')
        print(result)
        query[row] = {}
        for branch, count in result:
            query[row][branch] = count
    
    print(query) #prints {'B.Des': {'CSE': 1}, 'B.Tech': {'CSE': 1, 'ME': 1}} 
    
    return render(request, "members/year.html", {'data' : query})

def branch(request, year, branch):
    alumni = Profile.objects.filter(batch = year, branch = branch)
    print(alumni)
    return render(request, "members/branch.html", {'a':alumni})
