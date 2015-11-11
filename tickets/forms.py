from django import forms
from django.core.exceptions import ObjectDoesNotExist
from editions.models import Edition
from attendants.models import Attendant
from tickets.models import TicketType, Ticket


# TODO add UPM faculties
class TicketForm(forms.Form):
    edition = forms.CharField(max_length=4, required=True)
    name = forms.CharField(max_length=200, required=True)
    email = forms.EmailField(required=True)
    company = forms.CharField(max_length=255, required=False)
    university = forms.CharField(max_length=255, required=False)
    faculty = forms.CharField(max_length=255, required=False)
    matriculation_number = forms.CharField(max_length=8, required=False)
    ticket_type = forms.CharField(required=True)

    def clean_edition(self):
        edition = self.cleaned_data.get('edition', None)
        try:
            Edition.objects.get(year=edition)
            return edition
        except ObjectDoesNotExist:
            raise forms.ValidationError('edition does not exist')

    def clean_ticket_type(self):
        ticket_type = self.cleaned_data.get('ticket_type', None)
        try:
            TicketType.objects.get(pk=ticket_type)
            return ticket_type
        except ObjectDoesNotExist:
            raise forms.ValidationError('type does not exist')

    def clean(self):
        cleaned_data = super(TicketForm, self).clean()

        company = cleaned_data.get('company', None)
        university = cleaned_data.get('university', None)
        faculty = cleaned_data.get('faculty', None)
        matriculation_number = cleaned_data.get('matriculation_number', None)


        if not company and not university:
            raise forms.ValidationError('must specify either company or university')

        if faculty and not university:
            raise forms.ValidationError('must specify university')

        if matriculation_number and not university:
            raise forms.ValidationError('must specify university')

        if matriculation_number and not faculty:
            raise forms.ValidationError('must specify faculty')
