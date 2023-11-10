from django import forms
from django_registration.forms import RegistrationForm

from variables import validators


class CustomRegistrationForm(RegistrationForm):
    phone = forms.CharField(validators=[validators.phone_regex], max_length=9)

    class Meta(RegistrationForm.Meta):
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "phone",
            "password1",
            "password2",
        ]
