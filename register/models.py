from django.db import models

from TryIT import settings_secret


class RegisterCompany(models.Model):
    contact_name = models.CharField(max_length=255)
    company = models.CharField(max_length=255, blank=True)

    email = models.EmailField()
    phone = models.CharField(max_length=13)

    # Sponsorship
    SPONSOR_TYPE = settings_secret.SPONSOR_TYPE
    SPONSOR_DATE = settings_secret.SPONSOR_DATE
    sponsor = models.BooleanField(default=False)
    sponsor_type = models.CharField(max_length=50, blank=True, choices=SPONSOR_TYPE)
    sponsor_date = models.CharField(max_length=50, blank=True, choices=SPONSOR_DATE)

    # Type
    TYPE = (
        ('ponencia', 'Ponencia'),
        ('taller', 'Taller')
    )
    type = models.CharField(max_length=50, choices=TYPE, default=TYPE[0][0])
    topic = models.CharField(max_length=255)
    description = models.TextField()
    document = models.FileField(upload_to='documents/', blank=True)

    def __str__(self):
        return self.company + " - " + self.contact_name
