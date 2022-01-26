from django.shortcuts import render
from django.http import HttpRequest
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import DetailView
from django.db.models import Count
from .models import Publication, PublicationMedia


def index(request):
    publication_list = Publication.objects.filter(is_visible=True).order_by('-created')
    # paginator = Paginator(list, 10)

    # page = request.GET.get('page')
    # try:
    #     albums = paginator.page(page)
    # except PageNotAnInteger:
    #     albums = paginator.page(1) # If page is not an integer, deliver first page.
    # except EmptyPage:
    #     albums = paginator.page(paginator.num_pages) # If page is out of range (e.g.  9999), deliver last page of results.

    return render(request, "publications/index.html", {'publications': publication_list})


class PublicationDetail(DetailView):
    model = Publication

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(PublicationDetail, self).get_context_data(**kwargs)
        context['media'] = PublicationMedia.objects.filter(publication=self.object.id)
        return context


def handler404(request, exception):
    assert isinstance(request, HttpRequest)
    return render(request, 'handler404.html', None, None, 404)
