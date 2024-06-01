from django.shortcuts import render
from .models import Award


# Create your views here.
def index(request):
    awards = Award.objects.all()
    award_count = awards.count()
    return render(request, "awards/index.html", {"awards": awards, "award_count": award_count})


def award(request, id):
    award = Award.objects.get(award_id=id)
    return render(request, "awards/award.html", {"award": award})
