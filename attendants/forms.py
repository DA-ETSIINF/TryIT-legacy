from django import forms
from attendants.models import Attendant


class AttendantForm(forms.ModelForm):
    class Meta:
        model = Attendant
