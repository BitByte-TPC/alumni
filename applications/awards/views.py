from django.shortcuts import render ,redirect
from .models import Award

# Create your views here.
def index(request):
    return render(request, "awards/index.html")


def award(request, id):
    try:
        award = Award.objects.get(award_id=id)
        return render(request, "awards/award.html", {"award": award})
    except:
        return redirect('awards:index')
