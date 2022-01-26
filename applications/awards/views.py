from django.shortcuts import render
from .models import Award


# Create your views here.
def index(request):
    return render(request, "awards/index.html")


def award(request, id):
    award = Award.objects.get(award_id=id)
    return render(request, "awards/award.html", {"award": award})
