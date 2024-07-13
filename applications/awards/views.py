from django.shortcuts import render, redirect
from .models import Award

def index(request):
    awards = Award.objects.all()
    for award in awards:
        words = award.description.split()
        award.short_description = ' '.join(words[:50]) + ('...' if len(words) > 50 else '')

    award_count = awards.count()
    return render(request, "awards/index.html", {"awards": awards, "award_count": award_count})

def award(request, id):
    try:
        award = Award.objects.get(award_id=id)
        return render(request, "awards/award.html", {"award": award})
    except Award.DoesNotExist:
        return redirect('awards:index')