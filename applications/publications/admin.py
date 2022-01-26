import os
import uuid
import zipfile
from datetime import datetime
from zipfile import ZipFile

from django.contrib import admin
from django.core.files.base import ContentFile

from .models import Publication, PublicationMedia
from .forms import PublicationForm

@admin.register(Publication)
class PublicationModelAdmin(admin.ModelAdmin):
    form = PublicationForm
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title_stripped', 'thumb', 'created')
    list_filter = ('created',)

    def save_model(self, request, obj, form, change):
        if form.is_valid():
            publication = form.save(commit=False)
            publication.modified = datetime.now()
            publication.save()

            if form.cleaned_data['zip'] is not None:
                zip = zipfile.ZipFile(form.cleaned_data['zip'])
                for filename in sorted(zip.namelist()):

                    file_name = os.path.basename(filename)
                    if not file_name:
                        continue

                    data = zip.read(filename)
                    contentfile = ContentFile(data)

                    media = PublicationMedia()
                    media.publication = publication
                    media.alt = filename
                    filename = '{0}{1}.pdf'.format(publication.slug, str(uuid.uuid4())[-13:])
                    media.media.save(filename, contentfile)
                    media.save()
                zip.close() 
            super(PublicationModelAdmin, self).save_model(request, obj, form, change)

# In case image should be removed from album.
@admin.register(PublicationMedia)
class PublicationMediaModelAdmin(admin.ModelAdmin):
    list_display = ('alt', 'publication')
    list_filter = ('publication', 'created')