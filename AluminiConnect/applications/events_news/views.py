from django.shortcuts import render
from .models import Event
# Create your views here.
def index(request):
    return render(request, "events_news/home.html")

def event(request, id):
    e = Event.objects.get(event_id = id)
    return render(request, "events_news/event.html", vars(e))
