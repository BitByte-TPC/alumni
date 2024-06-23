from django.forms import ModelForm
from .models import Blog , Campaign


class BlogForm(ModelForm):
    class Meta:
        model =Blog
        fields = '__all__'
        exclude=['author']
        
class CampaignForm(ModelForm):
    class Meta:
        model =Campaign
        fields = '__all__'