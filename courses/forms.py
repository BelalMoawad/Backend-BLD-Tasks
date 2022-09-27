import email
from socket import fromshare
from unicodedata import name
from django import forms
from django.core.exceptions import ValidationError

def Validate_RangeLength(Data):
    if len(Data) < 10 or len(Data) > 500 :
        raise ValidationError(
            "You must enter data length between 10 and 500 inclusively",
             code="Not_Accepted_Value"
            )    


class CourseForm(forms.Form) :
    name = forms.CharField(min_length=10, max_length=50)
    description = forms.CharField(validators=[Validate_RangeLength])



class UserForm(forms.Form) :
    first_name = forms.CharField(min_length=3, max_length=15)
    last_name = forms.CharField(min_length=3, max_length=15)
    birth_date = forms.DateField()
    user_email = forms.EmailField()
    password = forms.CharField(min_length=5, max_length=20)