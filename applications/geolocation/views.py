import requests

try:
    from collections.abc import Counter
except ImportError:
    from collections import Counter

from django.shortcuts import render
from django.db.models import Count
from django.core import serializers
from applications.alumniprofile.models import Profile
from .models import MapPoints


# Create your views here.
def index(request):
    city = Profile.objects.only('city', 'state', 'country')
    city = Counter([f'{c.city} {c.state} {c.country}' for c in city])
    points = MapPoints.objects.all()
    data = []
    for pt in points:
        title = pt.city + ', ' + pt.state + ', ' + pt.country
        data = data + [{'city': pt.city, 'lat': pt.lat, 'lon': pt.long, 'count': city[f'{pt.city} {pt.state} {pt.country}'],
                        'title': title}]
    # print(data)
    return render(request, "geolocation/index.html", {'data': data})


def addPoints(point):
    msg = 'Error receiving point'
    if point:
        url = "https://nominatim.openstreetmap.org/search?format=json&limit=1&q="
        if not MapPoints.objects.filter(city=point['city'], state=point['state'], country=point['country']).exists():
            qry = point['city'] + '+' + point['state'] + '+' + point['country']
            # print(qry)
            pt = requests.get(url + qry).json()
            # print(pt)
            if pt:
                point = MapPoints(
                    city=point['city'],
                    state=point['state'],
                    country=point['country'],
                    lat=float(pt[0]['lat']),
                    long=float(pt[0]['lon']))
                point.save()
                msg = 'Map Point added'
            else:
                msg = 'Map Point not found'
        else:
            msg = 'Map Point already exists'
    return msg


def updatePoints(request):
    url = "https://nominatim.openstreetmap.org/search?format=json&limit=1&q="
    addr = Profile.objects.values('city', 'state', 'country')
    error = []
    skipped = []
    done = []
    for add in addr:
        # print(add, MapPoints.objects.filter(city=add['city'], state=add['state'], country=add['country']).exists())
        if not MapPoints.objects.filter(city=add['city'], state=add['state'], country=add['country']).exists():
            qry = add['city'] + '+' + add['state'] + '+' + add['country']
            # print(qry)
            pt = requests.get(url + qry).json()
            # print(pt)
            if pt:
                point = MapPoints(
                    city=add['city'],
                    state=add['state'],
                    country=add['country'],
                    lat=float(pt[0]['lat']),
                    long=float(pt[0]['lon']))
                point.save()
                done.append(add['city'])
                # print('done')
            else:
                # print('error')
                error.append(add['city'])
        else:
            # print('skipped')
            skipped.append(add['city'])
    print("\nThese new cities added:\n", done)
    print("\nThese cities already exists:\n", skipped)
    print("\nThese cities not found:\n", error)
    context = {'done': done,
               'skip': skipped,
               'error': error
               }
    return render(request, 'geolocation/index.html', context)
