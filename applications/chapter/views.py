import zipfile, uuid
from datetime import datetime
from zipfile import ZipFile
from PIL import Image

from django.conf import settings
from django.core.files.base import ContentFile
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.utils.html import strip_tags
from applications.alumniprofile.models import Profile
from applications.gallery.models import AlbumImage, Album
from .models import *
from .forms import *


# Create your views here.
def index(request):
    chapters = Chapters.objects.all()
    context = {
        'chapters': chapters,
    }
    return render(request, 'chapter/index.html', context)


def chapter_data(request, id):
    chapter = Chapters.objects.get(pk=id)
    post = ChapterTeam.objects.filter(chapter=chapter)
    event = ChapterEvent.objects.filter(chapter=chapter)
    album = ChapterAlbum.objects.filter(chapter=chapter)
    team = []
    for i in post:
        prof = Profile.objects.get(user=i.user)
        t = {'name': str(prof.name), 'post': str(i.post), 'email': str(prof.email),
             'pic': str(prof.profile_picture.url)}
        team.append(t)
    context = {
        'chapter': chapter,
        'team': team,
        'event': event,
        'album': album
    }
    if request.user.is_authenticated and ChapterTeam.objects.filter(chapter=chapter, user=request.user).exists():
        forms = {
            'eventf': EventForm(),
            'chapterf': DescriptionForm(instance=chapter),
            'albumf': AlbumForm()
        }
        context.update(forms)
    return context


def chapter(request, id):
    res = 'GET Request'
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        if 'chapter' in request.POST:
            res = chapter_edit(request, id)
        elif 'event' in request.POST:
            res = event_add(request, id)
        elif 'album' in request.POST:
            res = album_add(request, id)
        else:
            res = 'Unknown Form'
    print(res)
    # return render(request, 'chapter/chapter.html', context)
    return redirect('chapter:chapter_redirect', id=id)


def chapter_redirect(request, id):
    context = chapter_data(request, id)
    return render(request, 'chapter/chapter.html', context)


def chapter_images(request):
    if request.is_ajax():
        id = request.GET['album']
        album = Album.objects.get(pk=id)
        images = AlbumImage.objects.filter(album=album)
        data = []
        for i in images:
            data.append({'src': i.image.url, 'h': i.height, 'w': i.width})
    else:
        data = 'fail'
    return JsonResponse(data, safe=False)


def chapter_edit(request, id):
    if request.method == 'POST':
        chapter = Chapters.objects.get(pk=id)
        form = DescriptionForm(request.POST, request.FILES, instance=chapter)
        if form.is_valid():
            chapter = form.save()
            chapter.save()
            return 'Success'
        return 'Form is not Valid'
    return 'Request method is not POST'


def event_add(request, id):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        print(request.POST['start_date'], request.POST['end_date'])
        if form.is_valid():
            event = form.save()
            event.save()
            chapter = Chapters.objects.get(pk=id)
            chapter_event = ChapterEvent(chapter=chapter, event=event)
            chapter_event.save()
            return 'Success'
        else:
            print(form.errors)
            return 'Form is not Valid'
    return 'Request method is not POST'


def album_add(request, id):
    if request.method == 'POST':
        form = AlbumForm(request.POST, request.FILES)
        if form.is_valid():
            album = form.save(commit=False)
            album.created = datetime.now()
            album.is_visible = True
            album.slug = strip_tags(album.title)
            album.save()

            if form.cleaned_data['zip'] is not None:
                zip = zipfile.ZipFile(form.cleaned_data['zip'])
                for filename in sorted(zip.namelist()):

                    file_name = os.path.basename(filename)
                    if not file_name or file_name.startswith('.'):
                        continue

                    data = zip.read(filename)
                    contentfile = ContentFile(data)

                    img = AlbumImage()
                    img.album = album
                    img.alt = filename
                    filename = '{0}{1}.jpg'.format(album.slug, str(uuid.uuid4())[-13:])
                    img.image.save(filename, contentfile)

                    filepath = '{0}/Albums/{1}'.format(settings.MEDIA_ROOT, filename)
                    with Image.open(filepath) as i:
                        img.width, img.height = i.size

                    img.thumb.save('thumb-{0}'.format(filename), contentfile)
                    img.save()
                zip.close()

            chapter = Chapters.objects.get(pk=id)
            chapter_album = ChapterAlbum(chapter=chapter, album=album)
            chapter_album.save()
            return 'Success'
        return 'Form is not Valid'
    return 'Request method is not POST'
