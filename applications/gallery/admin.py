import os
import uuid
import zipfile
from datetime import datetime
from zipfile import ZipFile

from django.conf import settings
from django.contrib import admin
from django.core.files.base import ContentFile

from PIL import Image

from .models import Album, AlbumImage
from .forms import AlbumForm

@admin.register(Album)
class AlbumModelAdmin(admin.ModelAdmin):
    form = AlbumForm
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title_stripped', 'thumb', 'created')
    list_filter = ('created',)

    def save_model(self, request, obj, form, change):
        if form.is_valid():
            album = form.save(commit=False)
            album.modified = datetime.now()
            album.save()

            if form.cleaned_data['zip'] is not None:
                zip = zipfile.ZipFile(form.cleaned_data['zip'])
                for filename in sorted(zip.namelist()):

                    file_name = os.path.basename(filename)
                    if not file_name:
                        continue

                    if file_name.startswith('.'):
                        # don't load hidden files. Use everywhere `PIL.Image` is used.
                        # OSX create a hidden file corresponding to each file while creating a zip.
                        # ex: '__MACOSX/._IMG_20230913_161134165.jpg'
                        # TODO: might need a better approach to check if the file is an image file which
                        # PIL will be able to `.open()`. see: https://stackoverflow.com/q/889333/9890886
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
            super(AlbumModelAdmin, self).save_model(request, obj, form, change)

# In case image should be removed from album.
@admin.register(AlbumImage)
class AlbumImageModelAdmin(admin.ModelAdmin):
    list_display = ('alt', 'album')
    list_filter = ('album', 'created')