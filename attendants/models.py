from django.db import models
from editions.models import Edition


class Attendant(models.Model):
    edition = models.ForeignKey(Edition)
    name = models.CharField(max_length=200)
    email = models.EmailField()

    company = models.CharField(max_length=255, blank=True)
    university = models.CharField(max_length=255, blank=True)
    faculty = models.CharField(max_length=255, blank=True)
    matriculation_number = models.CharField(max_length=8, blank=True)

    class Meta:
        unique_together = ('edition', 'email')

    def __str__(self):
        return self.name

    def is_student(self):
        return self.university is not None

    def is_upm_student(self):
        return self.faculty is not None

    def is_etsiinf_student(self):
        return self.matriculation_number is not None
