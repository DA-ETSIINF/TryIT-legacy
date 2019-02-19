from django.db import models

# Create your models here.


class Event(models.Model):
    edition = models.ForeignKey("editions.Edition", on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class EventSession(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    date = models.DateTimeField()
    capacity = models.IntegerField()
    attendants = models.ManyToManyField("tickets.Attendant")
