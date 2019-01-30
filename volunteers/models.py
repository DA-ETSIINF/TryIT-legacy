from django.db import models

from editions.models import Edition
from tickets.models import School, Degree
from tickets.models import Validator


SHIRT_SIZE = (
		('s', 'S'),
		('m', 'M'),
		('l', 'L'),
		('xl', 'XL'),
		('xxl', 'XXL')
	)
# manytomanysessions


class VolunteerRole(models.Model):
    role = models.CharField(max_length=250)

    def __str__(self):
        return self.role


class Volunteer(models.Model):
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    expedient = models.CharField(max_length=20)
    email = models.EmailField()
    phone = models.CharField(max_length=13)
    school = models.ForeignKey(School, on_delete=models.PROTECT)
    degree = models.ForeignKey(Degree, on_delete=models.PROTECT)
    active = models.BooleanField(default=False)
    commentary = models.TextField(null=True)
    shirt_size = models.CharField(max_length=250, choices=SHIRT_SIZE, default='m')
    android_phone = models.BooleanField(default=False)
    rolelist = models.ManyToManyField(VolunteerRole, blank=True, editable=False)


    def __str__(self):
        return '{} {}'.format(self.name, self.surname)

    def save(self,  *args, **kwargs):
        super(Volunteer, self).save( *args, **kwargs)





class Schedule(models.Model):
    edition = models.ForeignKey(Edition, on_delete=models.CASCADE)
    type = models.CharField(max_length=255)

    def __str__(self):
        return '{} - {}'.format(self.edition, self.type)


class VolunteerSchedule(models.Model):
    volunteer = models.ForeignKey(Volunteer, on_delete=models.CASCADE)
    schedule = models.ForeignKey(Schedule, on_delete=models.PROTECT)
    day = models.DateField(null=False)

    def __str__(self):
        return '{} {} - {}: {}'.format(self.volunteer.name, self.volunteer.surname, self.day, self.schedule.type)

