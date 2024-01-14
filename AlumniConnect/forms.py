import re
from django import forms
from applications.alumniprofile.models import Profile, Constants, Batch
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Div, Field
from crispy_forms.bootstrap import InlineRadios
from django.core.exceptions import ValidationError

from applications.alumniprofile.models import Constants


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
        fields = ['batch', 'programme', 'branch']


class ProfileEdit(forms.ModelForm):
    date_of_birth = forms.DateField(
        widget=forms.TextInput(
            attrs={'type': 'date'}
        ),
        required=True,
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
            attrs={'rows': 3, 'placeholder': 'Enter Permanent Address', }
        ),
        max_length=4000,
        required=False,
    )
    country = forms.CharField(widget=forms.Select(
        attrs={'id': 'countryId', 'class': 'countries order-alpha custom-select'}))
    state = forms.CharField(
        widget=forms.Select(attrs={'id': 'stateId', 'class': 'states order-alpha custom-select'}))
    city = forms.CharField(
        widget=forms.Select(attrs={'id': 'cityId', 'class': 'cities order-alpha custom-selects'}))
    linkedin = forms.URLField(widget=forms.TextInput(attrs={'placeholder': 'Linkedin URL'}))
    website = forms.URLField(widget=forms.TextInput(attrs={'placeholder': 'Website'}), required=False)
    facebook = forms.URLField(widget=forms.TextInput(attrs={'placeholder': 'Facebook URL'}), required=False)
    instagram = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Instagram Username'}), required=False)
    custom_city = forms.CharField(widget=forms.TextInput(
        attrs={'id': 'city_input', 'class': 'cityInput', 'placeholder': 'Enter city name'}), required=False)
    checkbox_city = forms.BooleanField(widget=forms.CheckboxInput(
        attrs={'onchange': 'customCityCheckboxToggled()'}), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fathers_name'].label = "Father/Mother's Name"
        self.fields['spouse_name'].label = "Spouse's Name"
        self.fields['mobile1'].label = "Mobile No."
        self.fields['mobile2'].label = "Alternate Mobile No."
        self.fields['batch'].label = 'Year of Passing'
        self.fields['sex'].label = 'Gender'
        self.fields['phone_no'].label = 'Phone No.'
        self.fields['roll_no'].label = 'Roll No.'
        self.fields['date_of_birth'].label = 'Date of Birth'
        self.fields['year_of_admission'].label = 'Year of Admission'
        self.fields['alternate_email'].label = 'Alternate Email'
        self.fields['custom_city'].label = 'City'
        self.fields['checkbox_city'].label = 'Can\'t find your city'

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Field('roll_no', css_class="form-control", wrapper_class='col-md-4'),
                Field('name', css_class="form-control", wrapper_class='col-md-4'),
                Field('sex', css_class="custom-select", wrapper_class="col-md-4"),
                css_class='form-row',
            ),
            Div(
                Field('fathers_name', css_class="form-control", wrapper_class='col-md-6'),
                Field('spouse_name', css_class="form-control", wrapper_class='col-md-6'),
                css_class='form-row',
            ),
            Div(
                Field('date_of_birth', css_class="form-control", wrapper_class='col-md-4'),
                Field('year_of_admission', css_class="custom-select", wrapper_class='col-md-4'),
                Field('batch', css_class="custom-select", wrapper_class="col-md-4"),
                css_class='form-row',
            ),
            Div(
                Field('branch', css_class="custom-select", wrapper_class="col-md-6"),
                Field('programme', css_class="custom-select", wrapper_class="col-md-6"),
                css_class='form-row',
            ),
            Div(
                Field('mobile1', css_class="form-control", wrapper_class='col-md-4'),
                Field('mobile2', css_class="form-control", wrapper_class='col-md-4'),
                Field('phone_no', css_class="form-control", wrapper_class="col-md-4"),
                css_class='form-row',
            ),
            Div(
                Field('email', css_class="form-control", wrapper_class='col-md-6'),
                Field('alternate_email', css_class="form-control", wrapper_class='col-md-6'),
                css_class='form-row',
            ),
            Div(
                Field('current_address', css_class="form-control", wrapper_class='col-md'),
                css_class='form-row',
            ),
            Div(
                Field('country', wrapper_class="col-md-4"),
                Field('state', wrapper_class="col-md-4"),
                Field('city', wrapper_class="col-md-4"),
                Field('custom_city', wrapper_class='col-md-4'),
                'checkbox_city',
                css_class='form-row',
            ),
            Div(
                Field('permanent_address', css_class="form-control", wrapper_class='col-md'),
                css_class='form-row',
            ),
            InlineRadios('working_status'),
            Div(
                Field('current_position', css_class="form-control", wrapper_class='col-md-6 col-lg-4'),
                Field('current_organisation', css_class="form-control", wrapper_class='col-md-6 col-lg-4'),
                Field('date_of_joining', css_class="form-control", wrapper_class='col-md-6 col-lg-4'),
                Field('past_experience', css_class="form-control", wrapper_class="col-md-6 col-lg-4"),
                css_class='form-row',
            ),
            Div(
                Field('current_course', css_class="form-control", wrapper_class='col-md-6 col-lg-4'),
                Field('current_university', css_class="form-control", wrapper_class='col-md-6 col-lg-4'),
                css_class='form-row',
            ),
            Div(
                Field('linkedin', css_class="form-control", wrapper_class='col-md-6'),
                Field('website', css_class="form-control", wrapper_class='col-md-6'),
                css_class='form-row',
            ),
            Div(
                Field('facebook', css_class="form-control", wrapper_class='col-md-6'),
                Field('instagram', css_class="form-control", wrapper_class='col-md-6'),
                css_class='form-row',
            ),
            Field('profile_picture', css_class="w-100"),
            # 'profile_picture',
            Submit('submit', 'Save Changes'),
        )
        # def clean(self):

    #     super(ProfileEdit, self).clean() #if necessary
    #     del self._errors['country']
    #     del self._errors['city']
    #     del self._errors['state']
    #     return self.cleaned_data

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
            'instagram',
            'name',
            'fathers_name',
            'spouse_name',
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
            # 'name': forms.TextInput(attrs={ 'readonly':'readonly'}),
            # 'sex': forms.TextInput(attrs={ 'readonly':'readonly'}),
            'email': forms.TextInput(attrs={'readonly': 'readonly'}),
            'roll_no': forms.TextInput(attrs={'readonly': 'readonly'}),
            'year_of_admission': forms.TextInput(attrs={'readonly': 'readonly'}),
            'branch': forms.TextInput(attrs={'readonly': 'readonly'}),
            'programme': forms.TextInput(attrs={'readonly': 'readonly'}),
            'working_status': forms.RadioSelect(choices=Constants.WORKING_STATUS),
        }


class NewRegister(forms.ModelForm):
    def clean_roll_no(self):
        roll_no = self.cleaned_data.get('roll_no').lower()

        user = User.objects.filter(username=roll_no)
        if user:
            raise forms.ValidationError(
                'Profile with this roll number already exists.'
            )

        match = re.search('^[a-zA-Z0-9]{5,9}$', roll_no)
        if not match:
            raise forms.ValidationError(
                'Please enter your valid institute roll number.'
            )

        return roll_no
    
    def clean_city(self):
        city = self.cleaned_data.get('city')
        city_checkbox = self.data.get('city_checkbox')
        city_input = self.data.get('city_input')

        if city_checkbox == 'on':
            return city_input
        
        return city

    class Meta:
        model = Profile

        fields = [
            'roll_no',
            'name',
            'fathers_name',
            'spouse_name',
            'sex',
            'date_of_birth',

            'programme',
            'branch',
            'year_of_admission',
            'batch',

            'mobile1',
            'mobile2',
            'email',
            'alternate_email',
            'current_address',
            'country',
            'state',
            'city',
            'permanent_address',

            'working_status',
            'current_organisation',
            'current_position',
            'date_of_joining',
            'past_experience',
            # 'current_university',
            # 'current_course',

            'linkedin',
            'facebook',
            'instagram',
            'website',
            'profile_picture'
        ]


class PasswordResetRequestForm(forms.Form):
    roll_no = forms.IntegerField(label=("Roll No."))
    email = forms.CharField(label=("Email"), max_length=254)


class SignupForm(forms.ModelForm):
    role = forms.ChoiceField(choices=Constants.ROLE_CHOICES)
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_username(self):
        # username is Roll No. #
        username_value = self.cleaned_data['username'].lower()

        # Regex matching institution's roll no
        x = re.search("^2[0-9][bmpid][cemdns][scem][0-2cmpdtoe]\d{2}[w]?$|^[0-2]\d[0-2]\d{4}$", username_value)
        if x == None:
            raise ValidationError(
                'Please enter a valid roll no.'
            )

        # check if this username i.e roll_no already exists
        user = User.objects.filter(username=username_value)
        if user.exists():
            raise ValidationError(
                'User with entered roll no. already exists'
            )

        return username_value

    def clean_email(self):
        email = self.cleaned_data['email'].lower()

        if re.search("iiitdmj.ac.in$", email):
            raise ValidationError(
                'Institute email id is not accepted. Please enter your personal email id'
            )

        return email

    def clean_confirm_password(self):
        # cleaned_data = super(SignupForm, self).clean()
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise ValidationError(
                'Entered passwords do not match'
            )

        return confirm_password
