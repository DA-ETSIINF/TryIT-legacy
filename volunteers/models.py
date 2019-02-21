from django.db import models

from editions.models import Edition
from tickets.models import School, Degree, Attendant
from tickets.models import Validator


SHIRT_SIZE = (
		('s', 'S'),
		('m', 'M'),
		('l', 'L'),
		('xl', 'XL'),
		('xxl', 'XXL')
	)


SCHEDULE_LIST = (
    ( 'M', 'Morning'),
    ( 'T', 'Afternoon'),
)


class VolunteerRole(models.Model):
    role = models.CharField(max_length=250)

    def __str__(self):
        return self.role


class Volunteer(models.Model):
    identity = models.OneToOneField(Attendant, on_delete=models.PROTECT, primary_key=True,)
    active = models.BooleanField(default=False)
    commentary = models.TextField(null=True)
    shirt_size = models.CharField(max_length=250, choices=SHIRT_SIZE, default='m')
    android_phone = models.BooleanField(default=False)
    rolelist = models.ManyToManyField(VolunteerRole, blank=True, editable=False)

    if identity:
        def __str__(self):
            return '{} {}'.format(self.identity.name, self.identity.lastname)

    def save(self,  *args, **kwargs):
        super(Volunteer, self).save( *args, **kwargs)


class VolunteerSchedule(models.Model):
    volunteer = models.ForeignKey(Volunteer, on_delete=models.CASCADE)
    schedule = models.CharField(max_length=20, choices=SCHEDULE_LIST)
    day = models.DateField(null=False)

    if volunteer:
        def __str__(self):
            return '{} {} - {}: {}'.format(self.volunteer.identity.name, self.volunteer.identity.lastname,
                                           self.day, self.schedule)
