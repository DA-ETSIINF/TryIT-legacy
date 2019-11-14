from django.db import models

# Create your models here.
from editions.models import Edition


class Streaming(models.Model):
    edition = models.ForeignKey(Edition, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    url = models.URLField()


class Organizers(models.Model):
    edition = models.ManyToManyField(Edition)
    name = models.CharField(max_length=250)
    linkedin = models.CharField(max_length=250)
    picture = models.ImageField(null=False, blank=True)

