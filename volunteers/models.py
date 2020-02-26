from django.db import models

from editions.models import Edition


SCHEDULE_LIST = (
    ( 'M', 'Morning'),
    ( 'T', 'Afternoon'),
)


class VolunteerRole(models.Model):
    role = models.CharField(max_length=250)

    def __str__(self):
        return self.role


class VolunteerSchedule(models.Model):
    volunteer = models.ForeignKey('tickets.Attendant', on_delete=models.CASCADE)
    schedule = models.CharField(max_length=20, choices=SCHEDULE_LIST)
    day = models.DateField(null=False)

    if volunteer:
        def __str__(self):
            return '{} {} - {}: {}'.format(self.volunteer.name, self.volunteer.lastname,
                                           self.day, self.schedule)