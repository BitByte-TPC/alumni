from django import forms
from .models import Profile

class editProfile(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['batch', 'programme', 'branch', 'sex', 'date_of_birth', 'address', 'phone_no', 'current_city', 'current_organisation', 'current_university', 'current_position', 'linkedin', 'website', 'profile_picture', 'last_visit']
