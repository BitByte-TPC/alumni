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
    date_of_joining = forms.DateField(
        widget=forms.TextInput(     
            attrs={'type': 'date'} 
        ),
        required=False,
    )
    current_address = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 3, 'placeholder': 'Enter Address'}
        ),
        max_length=4000,
    )
    permanent_address = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 3, 'placeholder': 'Enter Permanent Address',}
        ),
        max_length=4000,
        required = False,
    )
    linkedin = forms.URLField(widget=forms.TextInput(attrs={'placeholder': 'Linkedin URL'}))
    website = forms.URLField(widget=forms.TextInput(attrs={'placeholder': 'Website'}),required = False)
    facebook = forms.URLField(widget=forms.TextInput(attrs={'placeholder': 'Facebook URL'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fathers_name'].label = "Father/Husband's Name"
        self.fields['mobile1'].label = "Mobile No."
        self.fields['mobile2'].label = "Alternate Mobile No."
        self.fields['batch'].label = 'Year of Passing'
        self.fields['sex'].label = 'Gender'
        self.fields['phone_no'].label = 'Phone No.'
        self.fields['roll_no'].label = 'Roll No.'
        self.fields['date_of_birth'].label = 'Date of Birth'
        self.fields['year_of_admission'].label = 'Year of Admission'
        self.fields['alternate_email'].label = 'Alternate Email'
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
                Column('year_of_admission', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('batch', css_class='form-group col-md-4 mb-0'),
                Column('programme', css_class='form-group col-md-4 mb-0'),
                Column('branch', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('mobile1', css_class='form-group col-md-4 mb-0'),
                Column('mobile2', css_class='form-group col-md-4 mb-0'),
                Column('phone_no', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),

            Row(
                Column('email', css_class='form-group col-md-6 mb-0'),
                Column('alternate_email', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('current_address', css_class='form-group col mb-0'),
                
                css_class='form-row'
            ),
            Row(
                Column('city', css_class='form-group col-md-4 mb-0'),
                Column('state', css_class='form-group col-md-4 mb-0'),
                Column('country', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('permanent_address', css_class='form-group col-md mb-0'),
            ),
            InlineRadios('working_status'),
            Row(
                Column('current_position', css_class='form-group col-md-3 mb-0'),
                Column('current_organisation', css_class='form-group col-md-3 mb-0'),
                Column('date_of_joining', css_class='form-group col-md-3 mb-0'),
                Column('past_experience', css_class='form-group col-md-3 mb-0'),
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
            ),
            Submit('submit', 'Save Changes'),
        )   

    class Meta:
        model = Profile

        fields = [
            'city',
            'country',
            'state',
            'year_of_admission',
            'alternate_email',
            'phone_no',
            'mobile1',
            'mobile2',
            'facebook',
            'name',
            'fathers_name',
            'sex',
            'email',
            'roll_no',
            'date_of_birth',
            'date_of_joining',
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
    date_of_joining = forms.DateField(
        widget=forms.TextInput(     
            attrs={'type': 'date'} 
        ),
        required=False,
    )
    current_address = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 3, 'placeholder': 'Enter Address'}
        ),
        max_length=4000,
    )
    permanent_address = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 3, 'placeholder': 'Enter Permanent Address',}
        ),
        max_length=4000,
        required = False,
    )
    country = forms.ChoiceField(widget=forms.Select(attrs={'id':'countryId','class':'countries order-alpha presel-IN','name':'country'}))
    state = forms.ChoiceField(widget=forms.Select(attrs={'id':'stateId','class':'states order-alpha','name':'state'}))
    city = forms.ChoiceField(widget=forms.Select(attrs={'id':'cityId','class':'cities order-alpha','name':'city'}))
    linkedin = forms.URLField(widget=forms.TextInput(attrs={'placeholder': 'Linkedin URL'}))
    website = forms.URLField(widget=forms.TextInput(attrs={'placeholder': 'Website'}), required = False)
    facebook = forms.URLField(widget=forms.TextInput(attrs={'placeholder': 'Facebook URL'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fathers_name'].label = "Father/Husband's Name"
        self.fields['mobile1'].label = "Mobile No."
        self.fields['mobile2'].label = "Alternate Mobile No."
        self.fields['batch'].label = 'Year of Passing'
        self.fields['sex'].label = 'Gender'
        self.fields['phone_no'].label = 'Phone No.'
        self.fields['roll_no'].label = 'Roll No.'
        self.fields['date_of_birth'].label = 'Date of Birth'
        self.fields['year_of_admission'].label = 'Year of Admission'
        self.fields['alternate_email'].label = 'Alternate Email'
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
                Column('year_of_admission', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('batch', css_class='form-group col-md-4 mb-0'),
                Column('programme', css_class='form-group col-md-4 mb-0'),
                Column('branch', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('mobile1', css_class='form-group col-md-4 mb-0'),
                Column('mobile2', css_class='form-group col-md-4 mb-0'),
                Column('phone_no', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),

            Row(
                Column('email', css_class='form-group col-md-6 mb-0'),
                Column('alternate_email', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('current_address', css_class='form-group col-md mb-0'),
                
                css_class='form-row'
            ),
            Row(
                Column('country', css_class='form-group col-md-4 mb-0'),
                Column('state', css_class='form-group col-md-4 mb-0'),
                Column('city', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('permanent_address', css_class='form-group col-md mb-0'),
                css_class='form-row'
            ),
            InlineRadios('working_status'),
            Row(
                Column('current_position', css_class='form-group col-md-3 mb-0'),
                Column('current_organisation', css_class='form-group col-md-3 mb-0'),
                Column('date_of_joining', css_class='form-group col-md-3 mb-0'),
                Column('past_experience', css_class='form-group col-md-3 mb-0'),
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
            ),
            'profile_picture',
            Submit('submit', 'Register'),
        )   

    def clean(self):
        super(NewRegister, self).clean() #if necessary
        del self._errors['country']
        del self._errors['city']
        del self._errors['state']
        return self.cleaned_data   

    class Meta:
        model = Profile

        fields = [
            'city',
            'country',
            'state',
            'year_of_admission',
            'alternate_email',
            'phone_no',
            'mobile1',
            'mobile2',
            'facebook',
            'name',
            'fathers_name',
            'sex',
            'email',
            'roll_no',
            'date_of_birth',
            'date_of_joining',
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