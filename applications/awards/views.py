# applications/awards/views.py
from django.shortcuts import render, redirect
from .models import Award

def index(request):
    awards = Award.objects.all()
    for award in awards:
        award.short_description = ' '.join(award.description.split()[:50]) 

    award_count = awards.count()
    return render(request, "awards/index.html", {"awards": awards, "award_count": award_count})

def award(request, id):
    try:
        award = Award.objects.get(award_id=id)
        return render(request, "awards/award.html", {"award": award})
    except Award.DoesNotExist:
        return redirect('awards:index')