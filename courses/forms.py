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
