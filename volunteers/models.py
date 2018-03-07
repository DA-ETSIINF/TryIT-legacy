from django.db import models

from editions.models import Edition
from tickets.models import School, Degree



SHIRT_SIZE = (
		('s', 'S'),
		('m', 'M'),
		('l', 'L'),
		('xl', 'XL'),
		('xxl', 'XXL')
	)

class Volunteer(models.Model):
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    expedient = models.CharField(max_length=20)
    email = models.EmailField()
    phone = models.CharField(max_length=13)
    school = models.ForeignKey(School)
    degree = models.ForeignKey(Degree)
    active = models.BooleanField(default=False)
    validator = models.ForeignKey("tickets.Validator", on_delete=models.SET_NULL, null=True, blank=True)
    commentary = models.TextField(null=True)
    shirt_size = models.CharField(max_length=250, choices=SHIRT_SIZE, default='m')
    android_phone  = models.BooleanField(default=False)

    def __str__(self):
        return '{} {}'.format(self.name, self.surname)
'''
    def save(self, *args, **kwargs):
        # generate key before save
        if self.validator and self.validator != self.req:
           self.validator=False
        if not  self.validator and self.validator != self.kwargs['validator'] :
            self.validator = True
            Validator.objects.create(
                name=self.name
            )
        super(Validator, self).save(*args, **kwargs)
'''



class Schedule(models.Model):
    edition = models.ForeignKey(Edition)
    type = models.CharField(max_length=255)

    def __str__(self):
        return '{} - {}'.format(self.edition, self.type)


class VolunteerSchedule(models.Model):
    volunteer = models.ForeignKey(Volunteer)
    schedule = models.ForeignKey(Schedule)
    day = models.DateField(null=False)

    def __str__(self):
        return '{} {} - {}: {}'.format(self.volunteer.name, self.volunteer.surname, self.day, self.schedule.type)
