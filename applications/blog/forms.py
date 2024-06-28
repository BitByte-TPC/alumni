from django import forms

class BlogSearchForm(forms.Form):
    username = forms.CharField(max_length=100, required=False, label='Author Username')
    title = forms.CharField(max_length=100, required=False, label='Title')
    tags = forms.CharField(max_length=100, required=False, label='Tags')
    campaign = forms.CharField(max_length=100, required=False, label='Campaign')
    is_self = forms.BooleanField(required=False, label='Self Blog')

    
