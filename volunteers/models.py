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
    school = models.ForeignKey(School)
    degree = models.ForeignKey(Degree)
    active = models.BooleanField(default=False)
    #validator = models.ForeignKey("tickets.Validator", on_delete=models.SET_NULL, null=True, blank=True)
    commentary = models.TextField(null=True)
    shirt_size = models.CharField(max_length=250, choices=SHIRT_SIZE, default='m')
    android_phone = models.BooleanField(default=False)
    rolelist = models.ManyToManyField(VolunteerRole, blank=True)

    old_rolelist = None

    def __init__(self, *args, **kwargs):
        super(Volunteer, self).__init__(*args, **kwargs)
        self.old_rolelist = self.rolelist

    def __str__(self):
        return '{} {}'.format(self.name, self.surname)

    def save(self,  force_insert=False, force_update=False, *args, **kwargs):
        # generate key before save
        role_validator = VolunteerRole.objects.get(role = "validator")
        super(Volunteer, self).save(force_insert, force_update, *args, **kwargs)

        if role_validator not in self.rolelist.all():
            print("coca")
            try:
                print("str "+ str(self.old_rolelist.get(role="validator")))

            except:
                print("Cocacola")
                Validator.objects.create(
                    name=self.name,
                    volunteer=self
                )
            else:
                pass





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

