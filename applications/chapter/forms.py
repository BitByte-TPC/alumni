from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from tempus_dominus.widgets import DateTimePicker
from applications.gallery.models import Album
from applications.events_news.models import Event
from .models import Chapters


class DescriptionForm(forms.ModelForm):
    description = forms.CharField(
        widget=CKEditorUploadingWidget(
            attrs={'id': 'chapter_description'}
        ),
        required=False
    )

    class Meta:
        model = Chapters
        fields = ['description', 'wall_picture']


class EventForm(forms.ModelForm):
    description = forms.CharField(
        widget=CKEditorUploadingWidget(
            attrs={'id': 'event_description'}
        )
    )
    title = forms.CharField(
        widget=CKEditorUploadingWidget(
            attrs={'id': 'event_title'}
        )
    )
    start_date = forms.DateTimeField(
        widget=DateTimePicker(
            options={
                'useCurrent': True,
                'format': 'YYYY-MM-DD HH:mm:ss',
                'icons': {
                    'time': 'fa fa-clock',
                    'today': 'fa fa-calendar-check',
                    'clear': 'fa fa-trash'
                }
            },
            attrs={
                'append': 'fa fa-calendar'
            }
        ),
    )
    end_date = forms.DateTimeField(
        widget=DateTimePicker(
            options={
                'useCurrent': True,
                'format': 'YYYY-MM-DD HH:mm:ss',
                'icons': {
                    'time': 'fa fa-clock',
                    'today': 'fa fa-calendar-check',
                    'clear': 'fa fa-trash'
                }
            },
            attrs={
                'append': 'fa fa-calendar'
            }
        ),
    )

    class Meta:
        model = Event
        exclude = []


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        exclude = ['slug', 'is_visible', 'created', ]

    zip = forms.FileField(required=False)
