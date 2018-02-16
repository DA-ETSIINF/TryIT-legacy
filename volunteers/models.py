from django.db import models


class RegisterVolunteers(models.Model):
    day = models.DateField(null=False)
    morning = models.BooleanField()
    afternoon = models.BooleanField()
    allday = models.BooleanField()

