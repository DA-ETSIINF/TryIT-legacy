from django.db import models
from TryIT.settings_edition import  SPONSOR_DATE, SPONSOR_TYPE, TYPE


class RegisterCompany(models.Model):
    contact_name = models.CharField(max_length=255)
    company = models.CharField(max_length=255, blank=True)

    email = models.EmailField()
    phone = models.CharField(max_length=13)

    # Sponsorship


    sponsor = models.BooleanField(default=False)
    sponsor_type = models.CharField(max_length=50, blank=True, choices=SPONSOR_TYPE)
    sponsor_date = models.CharField(max_length=50, blank=True, choices=SPONSOR_DATE)

    # Type

    type = models.CharField(max_length=50, choices=TYPE, default=TYPE[0][0])
    topic = models.CharField(max_length=255)
    description = models.TextField()
    document = models.FileField(upload_to='documents/', blank=True)

    def __str__(self):
        return self.company + " - " + self.contact_name
