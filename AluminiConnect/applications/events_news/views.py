from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Event, Attendees
from django.db.models import Count
from django.contrib.auth.models import User
# Create your views here.
def events(request):
    events_list = Event.objects.filter()
    return render(request, "events_news/index.html", {'events' : events_list})

def event(request, id):
    e = Event.objects.get(event_id = id)
    attending = Attendees.objects.filter(event_id = e)
    check = False
    if request.user.is_authenticated:
        if Attendees.objects.get(user_id = User.objects.get(username=request.user.username), event_id = e):
            check = True
    
    if request.POST.get("submit") == "rsvp":
        if not request.user.is_authenticated:
            return HttpResponseRedirect("/login/?next="+request.path)

        attendee = Attendees()
        attendee.user_id = User.objects.get(username = request.user.username)
        attendee.event_id = Event.objects.get(event_id = id)
        attendee.save()

    return render(request, "events_news/event.html", {"event" : e, "check":check, "count":attending.count()})
