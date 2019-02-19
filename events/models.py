from django.db import models

# Create your models here.


class EventType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Event(models.Model):
    edition = models.ForeignKey("editions.Edition", on_delete=models.CASCADE)
    type = models.ForeignKey(EventType, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class EventSession(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    date = models.DateTimeField()
    capacity = models.IntegerField()
    attendants = models.ManyToManyField("tickets.Attendant", blank=True, null=True)
    attendants = models.ManyToManyField("tickets.Attendant", blank=True, null=True)


