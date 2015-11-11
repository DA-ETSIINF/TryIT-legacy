import hashlib
from django.db import models
from editions.models import Edition, SessionFormat, Session
from attendants.models import Attendant
from django.utils.crypto import get_random_string
from django.dispatch import receiver
from django.db.models.signals import pre_save


class Validator(models.Model):
    name = models.CharField(max_length=255)
    secret_key = models.CharField(max_length=256, default=get_random_string(256))

    def __str__(self):
        return self.name


class TicketType(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    # valid for this edition
    edition = models.ForeignKey(Edition)
    # valid for these session formats
    session_formats = models.ManyToManyField(SessionFormat, blank=True)
    # valid for these sessions
    sessions = models.ManyToManyField(Session, blank=True)
    # valid between
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)

    available_amount = models.PositiveIntegerField(default=100)
    price = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name + " " + self.edition.year


class Ticket(models.Model):
    time_stamp = models.DateTimeField(auto_now_add=True)

    type = models.ForeignKey(TicketType)

    attendant = models.ForeignKey(Attendant)

    secret_key = models.CharField(max_length=256, default=get_random_string(256))
    signature = models.CharField(max_length=256, blank=True)

    def __str__(self):
        return self.type.name

    def sign(self):
        key = '%s%s%s%s%s' % (str(self.time_stamp), str(self.pk), self.attendant.name, self.attendant.email, self.secret_key)
        sha1 = hashlib.sha1(key.encode('utf-8'))
        self.signature = sha1.hexdigest().upper()

    def save(self, *args, **kwargs):
        # sign before save
        self.sign()
        super(Ticket, self).save(*args, **kwargs)


class CheckIn(models.Model):
    time_stamp = models.DateTimeField(auto_now_add=True)

    attendant = models.ForeignKey(Attendant)
    session = models.ForeignKey(Session)

    def __str__(self):
        return str(self.time_stamp) + " - " + self.attendant.name + " - " + self.session.title
