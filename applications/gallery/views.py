from django.shortcuts import render
from django.http import HttpRequest
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import DetailView
from django.db.models import Count
from .models import Album, AlbumImage


def gallery(request):
    album_list = Album.objects.filter(is_visible=True).order_by('-created').annotate(images_count=Count('albumimage'))
    # paginator = Paginator(list, 10)

    # page = request.GET.get('page')
    # try:
    #     albums = paginator.page(page)
    # except PageNotAnInteger:
    #     albums = paginator.page(1) # If page is not an integer, deliver first page.
    # except EmptyPage:
    #     albums = paginator.page(paginator.num_pages) # If page is out of range (e.g.  9999), deliver last page of results.

    return render(request, "gallery/index.html", {'albums': album_list})


class AlbumDetail(DetailView):
    model = Album

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(AlbumDetail, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the images
        images = AlbumImage.objects.filter(album=self.object.id)
        context['images'] = images
        context['images_count'] = images.count()
        return context


def handler404(request, exception):
    assert isinstance(request, HttpRequest)
    return render(request, 'handler404.html', None, None, 404)
