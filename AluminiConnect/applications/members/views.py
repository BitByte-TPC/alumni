from django.shortcuts import render
from django.db.models import Count
from applications.alumniprofile.models import Profile
# Create your views here.

def index(request):
    counts = Profile.objects.values('batch').order_by('-batch').annotate(count = Count('batch'))
    return render(request, "members/index.html", {'data' : counts.values_list('batch', 'count')})

def batch(request, year):
    programmes = Profile.objects.filter(batch = year).values_list('programme', flat=True).distinct()
    query = {}
    for row in programmes:
        result = Profile.objects.filter(batch = year,programme = row).values_list('branch').annotate(count = Count('branch'))
        query[row] = {}
        for branch, count in result:
            query[row][branch] = count
    
    print(query) #prints {'B.Des': {'CSE': 1}, 'B.Tech': {'CSE': 1, 'ME': 1}} 

    return render(request, "members/year.html", {'data' : query })

