from django.db import models

from tickets.models import School, Degree


class Volunteer(models.Model):
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    expedient = models.CharField(max_length=20)
    email = models.EmailField()
    phone = models.CharField(max_length=13)
    school = models.ForeignKey(School)
    degree = models.ForeignKey(Degree)


class RegisterVolunteers(models.Model):
    day = models.DateField(null=False)
    morning = models.BooleanField()
    afternoon = models.BooleanField()
    allday = models.BooleanField()