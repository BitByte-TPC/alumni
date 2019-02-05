from django import forms
from applications.alumniprofile.models import Profile, Constants
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column


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

class RegisterForm1(forms.ModelForm):
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('first_name', css_class='form-group col-md-4 mb-0'),
                Column('last_name', css_class='form-group col-md-4 mb-0'),
                Column('sex', css_class='form-group col-md-4 mb-0'),
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
                Column('phone_no', css_class='form-group col-md-6 mb-0'),
                Column('current_city', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('current_position', css_class='form-group col-md-6 mb-0'),
                Column('current_organisation', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('linkedin', css_class='form-group col-md-6 mb-0'),
                Column('website', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),Row(
                Column('profile_picture', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Save Changes'),
        )

    class Meta:
        model = Profile
        fields = ['first_name','last_name','sex','email','roll_no','date_of_birth','branch','programme','batch','current_address','permanent_address','phone_no','current_city','current_position','current_organisation','linkedin','website','profile_picture']
        widgets = {
            'first_name': forms.TextInput(attrs={ 'readonly':'readonly'}),
            'last_name': forms.TextInput(attrs={ 'readonly':'readonly'}),
            'sex': forms.TextInput(attrs={ 'readonly':'readonly'}),
            'email': forms.TextInput(attrs={ 'readonly':'readonly'}),
            'roll_no': forms.TextInput(attrs={ 'readonly':'readonly'}),
            'date_of_birth': forms.TextInput(attrs={ 'readonly':'readonly'}),
            'branch': forms.TextInput(attrs={ 'readonly':'readonly'}),
            'programme': forms.TextInput(attrs={ 'readonly':'readonly'}),
            'batch': forms.TextInput(attrs={ 'readonly':'readonly'}),
        }