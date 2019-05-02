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
    if len(key) < 3:
        return render(request, "members/search.html", {'val': key })
    words = (w.strip() for w in key.split())
    name_q = Q()
    for token in words:
        name_q = name_q & (Q(first_name__icontains=token) | Q(last_name__icontains=token))
    search_results = User.objects.filter(name_q)
    print (search_results)
    search = Profile.objects.filter(user_id__in=search_results)
    print(search)
    if len(search_results) == 0:
        search_results = []
    context = { 'data':search,
                'val':key,
            }
    return render(request,"members/search.html",context)