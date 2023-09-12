from django import forms
from .models import ApplicationDetails

class ApplicationDetailsForm(forms.ModelForm):
    class Meta:
        model = ApplicationDetails
        fields = ['name', 'email', 'country_code', 'phone', 'course']