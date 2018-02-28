from django.db import models

from editions.models import Edition
from tickets.models import School, Degree


class Volunteer(models.Model):
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    expedient = models.CharField(max_length=20)
    email = models.EmailField()
    phone = models.CharField(max_length=13)
    school = models.ForeignKey(School)
    degree = models.ForeignKey(Degree)
    active = models.BooleanField(default=False)
    validator = models.BooleanField(default=False)
    commentary = models.TextField(null=True)


class Schedule(models.Model):
    edition = models.ForeignKey(Edition)
    type = models.CharField(max_length=255)

    def __str__(self):
        return '{} - {}'.format(self.edition, self.type)


class VolunteerSchedule(models.Model):
    volunteer = models.ForeignKey(Volunteer)
    schedule = models.ForeignKey(Schedule)
    day = models.DateField(null=False)
