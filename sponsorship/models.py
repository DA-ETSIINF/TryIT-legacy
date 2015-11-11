from django.db import models
from editions.models import Company, Edition


class Sponsorship(models.Model):
    edition = models.ForeignKey(Edition)
    name = models.CharField(max_length=200)
    price = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name + " " + self.edition.year


class Sponsor(models.Model):
    company = models.ForeignKey(Company)
    sponsorship = models.ForeignKey(Sponsorship)
    amount = models.PositiveIntegerField()

    def __str__(self):
        return self.company.name + " " + self.sponsorship.name + " " + self.sponsorship.edition.year


class Partner(models.Model):
    company = models.ForeignKey(Company)
    edition = models.ForeignKey(Edition)

    def __str__(self):
        return self.company.name + " " + self.edition.year
