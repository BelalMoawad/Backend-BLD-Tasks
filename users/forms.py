from enum import unique
from django import forms
from django.core.exceptions import ValidationError

class UserForm(forms.Form) :
    first_name = forms.CharField(min_length=3, max_length=15)
    last_name = forms.CharField(min_length=3, max_length=15)
    birth_date = forms.DateField()
    user_email = forms.EmailField()
    password = forms.CharField(min_length=5, max_length=20)