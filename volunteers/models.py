from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='logosCompanys', blank=True, null=True)

    url = models.URLField(blank=True)
    url_cv = models.URLField(blank=True)

    contact_person = models.CharField(max_length=200, blank=True)
    contact_email = models.EmailField(blank=True)
    phone_number = models.CharField(max_length=12, blank=True)

    def __str__(self):
        return self.name


class Volunteer(models.Model):
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    expedient = models.CharField(max_length=20)
    email = models.EmailField()
    phone = models.CharField(max_length=13)

class RegisterVolunteers(models.Model):
    day = models.DateField(null=False)
    morning = models.BooleanField()
    afternoon = models.BooleanField()
    allday = models.BooleanField()