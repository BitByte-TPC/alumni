from django.shortcuts import render
from .models import Event
# Create your views here.
def events(request):
    events_list = Event.objects.filter()
    return render(request, "events_news/index.html", {'events' : events_list})

def event(request, id):
    e = Event.objects.get(event_id = id)
    return render(request, "events_news/event.html", vars(e))
