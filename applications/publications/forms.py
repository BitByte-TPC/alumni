from django import forms
from .models import Publication


class PublicationForm(forms.ModelForm):
    class Meta:
        model = Publication
        exclude = []

    zip = forms.FileField(required=False)
