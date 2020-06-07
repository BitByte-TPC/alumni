from django.shortcuts import render
from django.http import JsonResponse
from applications.alumniprofile.models import Profile
from applications.gallery.models import AlbumImage,Album
from .models import *

# Create your views here.
def index(request):
    chapters = Chapters.objects.all()
    context = {
        'chapters' : chapters,
    }
    print("Yaaha Pahucha")
    return render(request, 'chapter/index.html',context)

def chapter(request, id):
    chapter = Chapters.objects.get(pk=id)
    post = ChapterTeam.objects.filter(chapter = chapter)
    event = ChapterEvent.objects.filter(chapter=chapter)
    album = ChapterAlbum.objects.filter(chapter=chapter)
    team = []
    for i in post:
        prof = Profile.objects.get(user=i.user)
        t = {'name':str(prof.name), 'post':str(i.post), 'email':str(prof.email), 'pic':str(prof.profile_picture.url)}
        team.append(t)
    context = {
        'chapter' : chapter,
        'team' : team,
        'event' : event,
        'album' : album
    }
    return render(request, 'chapter/chapter.html', context)

def chapter_images(request):
    if request.is_ajax():
        id = request.GET['album']
        album = Album.objects.get(pk=id)
        images = AlbumImage.objects.filter(album=album)
        data = []
        for i in images:
            data.append({'src':i.image.url, 'h':i.height, 'w':i.width})
    else:
        data= 'fail'
    return JsonResponse(data,safe = False)
