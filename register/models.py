from django.db import models


class RegisterCompany(models.Model):
    contact_name = models.CharField(max_length=255)
    company = models.CharField(max_length=255, blank=True)

    email = models.EmailField()
    phone = models.CharField(max_length=13)

    # Sponsorship
    SPONSOR_TYPE = (
        ('oro', 'ORO'),
        ('plata', 'PLATA'),
        ('bronce', 'BRONCE')
    )
    SPONSOR_DATE = (
        ('13/03/2017', '13/03/2017'),
        ('14/03/2017', '14/03/2017'),
        ('15/03/2017', '15/03/2017'),
        ('16/03/2017', '16/03/2017'),
        ('17/03/2017', '17/03/2017')
    )
    sponsor = models.BooleanField(default=False)
    sponsor_type = models.CharField(max_length=50, blank=True, choices=SPONSOR_TYPE)
    sponsor_date = models.CharField(max_length=50, blank=True, choices=SPONSOR_DATE)
    topic = models.CharField(max_length=255)
    description = models.TextField()
    document = models.FileField(upload_to='documents/', blank=True)

    def __str__(self):
        return self.company + "-" + self.contact_name
