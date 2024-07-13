from django.forms import forms ,ModelForm
from .models import Blog , Campaign
from django.utils.timezone import now

class BlogForm(ModelForm):
    class Meta:
        model =Blog
        fields = '__all__'
        exclude=['author']
        
    def clean(self):
        cleaned_data = super().clean()
        blog_type = cleaned_data.get('blog_type')
        campaign_id = cleaned_data.get('campaign_id')

        if blog_type == 'C' and not campaign_id:
            raise forms.ValidationError('Campaign is required for campaign blog type.')

        return cleaned_data
        
class CampaignForm(ModelForm):
    class Meta:
        model =Campaign
        fields = '__all__'
    
    def clean(self):
        cleaned_data = super().clean()
        date_started = now()
        date_ended = cleaned_data.get('date_ended')
        
        if date_ended is None:
            raise forms.ValidationError('End Date is required')

        if date_ended is not None and date_ended <= date_started:
            raise forms.ValidationError('End date must be greater or equal to Today\'s date.')

        return cleaned_data