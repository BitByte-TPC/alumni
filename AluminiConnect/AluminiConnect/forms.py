from django import forms

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