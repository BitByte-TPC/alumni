import datetime
from django import forms
from applications.alumniprofile.models import Profile, Constants, Batch
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from crispy_forms.bootstrap import InlineRadios



class UserRegistrationForm(forms.Form):
    username = forms.CharField(
        required = True,
        label = 'Roll No',
        max_length = 8,
    )
    email = forms.CharField(
        required = True,
        label = 'Email Addresss',
        max_length = 32,
    )

    password =  forms.CharField(
        required = True,
        label = 'Passsword',
        max_length = 32,
        min_length = 8,
        widget = forms.PasswordInput(),
    )

class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('batch', css_class='form-group col-md-4 mb-0'),
                Column('programme', css_class='form-group col-md-4 mb-0'),
                Column('branch', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Search', css_class=''),
        )

    class Meta:
        model = Profile
        fields = ['batch','programme','branch']


class ProfileEdit(forms.ModelForm):
    current_address = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 5, 'placeholder': 'Enter Address'}
        ),
        max_length=4000,
    )
    permanent_address = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 5, 'placeholder': 'Enter Permanent Address',}
        ),
        max_length=4000,
    )
    linkedin = forms.URLField(widget=forms.TextInput(attrs={'placeholder': 'Linkedin URL'}))
    website = forms.URLField(widget=forms.TextInput(attrs={'placeholder': 'Website'}))
    facebook = forms.URLField(widget=forms.TextInput(attrs={'placeholder': 'Facebook URL'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fathers_name'].label = "Father/Husband's Name"
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-4 mb-0'),
                Column('sex', css_class='form-group col-md-4 mb-0'),
                Column('fathers_name', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('roll_no', css_class='form-group col-md-4 mb-0'),
                Column('date_of_birth', css_class='form-group col-md-4 mb-0'),
                Column('email', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('batch', css_class='form-group col-md-4 mb-0'),
                Column('programme', css_class='form-group col-md-4 mb-0'),
                Column('branch', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('current_address', css_class='form-group col-md-6 mb-0'),
                Column('permanent_address', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('city', css_class='form-group col-md-6 mb-0'),
                Column('state', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('country', css_class='form-group col-md-6 mb-0'),
                Column('phone_no', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('alternate_phone_no', css_class='form-group col-md-6 mb-0'),
                Column('alternate_email', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            InlineRadios('working_status'),
            Row(
                Column('current_position', css_class='form-group col-md-4 mb-0'),
                Column('current_organisation', css_class='form-group col-md-4 mb-0'),
                Column('past_experience', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('current_course', css_class='form-group col-md-4 mb-0'),
                Column('current_university', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('linkedin', css_class='form-group col-md-4 mb-0'),
                Column('facebook', css_class='form-group col-md-4 mb-0'),
                Column('website', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),Row(
                Column('profile_picture', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Save Changes'),
        )   

    class Meta:
        model = Profile

        fields = [
            'alternate_email',
            'alternate_phone_no',
            'facebook',
            'name',
            'fathers_name',
            'sex',
            'email',
            'roll_no',
            'date_of_birth',
            'working_status',
            'branch',
            'programme',
            'batch',
            'current_address',
            'permanent_address',
            'phone_no',
            'city',
            'country',
            'state',
            'current_position',
            'current_organisation',
            'past_experience',
            'current_course',
            'current_university',
            'linkedin',
            'website',
            'profile_picture']

        widgets = {
            'name': forms.TextInput(attrs={ 'readonly':'readonly'}),
            'sex': forms.TextInput(attrs={ 'readonly':'readonly'}),
            'email': forms.TextInput(attrs={ 'readonly':'readonly'}),
            'roll_no': forms.TextInput(attrs={ 'readonly':'readonly'}),
            'date_of_birth': forms.TextInput(attrs={ 'readonly':'readonly'}),
            'branch': forms.TextInput(attrs={ 'readonly':'readonly'}),
            'programme': forms.TextInput(attrs={ 'readonly':'readonly'}),
            'batch': forms.TextInput(attrs={ 'readonly':'readonly'}),
            'working_status': forms.RadioSelect(choices=Constants.WORKING_STATUS),
        }


class NewRegister(forms.ModelForm):
    date_of_birth = forms.DateField(
        widget=forms.TextInput(     
            attrs={'type': 'date'} 
        ),
    )
    current_address = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 5, 'placeholder': 'Enter Address'}
        ),
        max_length=4000,
    )
    permanent_address = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 5, 'placeholder': 'Enter Permanent Address',}
        ),
        max_length=4000,
    )
    linkedin = forms.URLField(widget=forms.TextInput(attrs={'placeholder': 'Linkedin URL'}))
    website = forms.URLField(widget=forms.TextInput(attrs={'placeholder': 'Website'}))
    facebook = forms.URLField(widget=forms.TextInput(attrs={'placeholder': 'Facebook URL'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fathers_name'].label = "Father/Husband's Name"
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-4 mb-0'),
                Column('sex', css_class='form-group col-md-4 mb-0'),
                Column('fathers_name', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('roll_no', css_class='form-group col-md-4 mb-0'),
                Column('date_of_birth', css_class='form-group col-md-4 mb-0'),
                Column('email', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('batch', css_class='form-group col-md-4 mb-0'),
                Column('programme', css_class='form-group col-md-4 mb-0'),
                Column('branch', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('current_address', css_class='form-group col-md-6 mb-0'),
                Column('permanent_address', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('city', css_class='form-group col-md-6 mb-0'),
                Column('state', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('country', css_class='form-group col-md-6 mb-0'),
                Column('phone_no', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('alternate_phone_no', css_class='form-group col-md-6 mb-0'),
                Column('alternate_email', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            InlineRadios('working_status'),
            Row(
                Column('current_position', css_class='form-group col-md-4 mb-0'),
                Column('current_organisation', css_class='form-group col-md-4 mb-0'),
                Column('past_experience', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('current_course', css_class='form-group col-md-4 mb-0'),
                Column('current_university', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('linkedin', css_class='form-group col-md-4 mb-0'),
                Column('facebook', css_class='form-group col-md-4 mb-0'),
                Column('website', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),Row(
                Column('profile_picture', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Register'),
        )   


    class Meta:
        model = Profile

        fields = [
            'city',
            'country',
            'state',
            'alternate_email',
            'alternate_phone_no',
            'facebook',
            'name',
            'fathers_name',
            'sex',
            'email',
            'roll_no',
            'date_of_birth',
            'working_status',
            'branch',
            'programme',
            'batch',
            'current_address',
            'permanent_address',
            'phone_no',
            'current_position',
            'current_organisation',
            'past_experience',
            'current_course',
            'current_university',
            'linkedin',
            'website',
            'profile_picture']

        widgets = {
            'working_status': forms.RadioSelect(choices=Constants.WORKING_STATUS),
        }