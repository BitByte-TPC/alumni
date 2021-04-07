from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Event, Attendees
from applications.gallery.models import Album, AlbumImage
from django.db.models import Count
from django.contrib.auth.models import User
from applications.alumniprofile.models import Profile
from django.utils import timezone
from itertools import chain


# Create your views here.
def events(request):
    now = timezone.now()
    events = Event.objects.filter(start_date__gte=now).order_by('start_date').annotate(Count('attendees__user_id'))
    # events_current = Event.objects.filter(start_date__lt=now).filter(end_date__gte=now).order_by('start_date')
    events_completed = Event.objects.filter(end_date__lt=now).order_by('-start_date').annotate(
        Count('attendees__user_id'))
    events_ongoing = Event.objects.filter(start_date__lte=now, end_date__gte=now).order_by('start_date').annotate(
        Count('attendees__user_id'))
    events_to_display = list(chain(events_ongoing, events, events_completed))
    return render(request, "events_news/index.html", {'events': events_to_display})


def event(request, id):
    e = Event.objects.get(event_id=id)
    attending = Attendees.objects.filter(event_id=e).values('user_id__profile__name',
                                                            'user_id__profile__profile_picture', 'user_id__id',
                                                            'user_id__username')  # .exclude(user_id__profile__name=None)
    attendees_limit = 5
    images_limit = 6
    check = False
    album_present = True
    try:
        album = Album.objects.get(event_id=e)
        images = AlbumImage.objects.filter(album=album.id)[:images_limit]
    except:
        album_present = False
        images = list()
        album = ""
    if request.user.is_authenticated:
        try:
            if Attendees.objects.get(user_id=User.objects.get(username=request.user.username), event_id=e):
                check = True
        except:
            pass

    if request.POST.get("submit") == "rsvp":
        if not request.user.is_authenticated:
            return HttpResponseRedirect("/login/?next=" + request.path)

        attendee = Attendees()
        attendee.user_id = User.objects.get(username=request.user.username)
        attendee.event_id = Event.objects.get(event_id=id)
        attendee.save()
        check = True
        return HttpResponseRedirect("/events/event/" + id + "/")

    if request.POST.get("submit") == "rsvp_del":
        if not request.user.is_authenticated:
            return HttpResponseRedirect("/login/?next=" + request.path)

        Attendees.objects.filter(
            user_id=User.objects.get(username=request.user.username),
            event_id=Event.objects.get(event_id=id)
        ).delete()
        return HttpResponseRedirect("/events/event/" + id + "/")

    return render(request, "events_news/event.html", {
        "event": e,
        "check": check,
        "count": attending.count(),
        "count_difference": attending.count() - attendees_limit,
        "attendees": attending,
        "attendees_sliced": attending[:attendees_limit],
        "album_present": album_present,
        "images": images,
        "album": album,
        "base_uri": request.build_absolute_uri()
    })
