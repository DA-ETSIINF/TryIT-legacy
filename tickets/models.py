import hashlib

from django.db import models
from django.utils.crypto import get_random_string
import hashlib
import json

from editions.models import Edition, SessionFormat, Session
from tickets.functions import secret_key_mail
from volunteers.models import VolunteerRole

SHIRT_SIZE = (
		('s', 'S'),
		('m', 'M'),
		('l', 'L'),
		('xl', 'XL'),
		('xxl', 'XXL')
	)


class Validator(models.Model):

    name = models.CharField(max_length=255, editable=False)
    secret_key = models.CharField(max_length=16, editable=False)
    volunteer = models.OneToOneField("Attendant", on_delete=models.PROTECT, null=True)

    def __str__(self):
        return str(self.pk) + " - " + self.name

    def save(self, *args, **kwargs):
        # generate key before save
        self.secret_key = get_random_string(16)
        if self.volunteer:
            secret_key_mail(self.secret_key, self.volunteer.edition, self.volunteer.email)
        super(Validator, self).save(*args, **kwargs)


class Attendant(models.Model):
    edition = models.ForeignKey(Edition, on_delete=models.PROTECT)
    name = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    student_id = models.CharField(max_length=200)
    email = models.EmailField()
    is_student = models.BooleanField(default=False)
    is_upm_student = models.BooleanField(default=False)
    print_accreditation = models.BooleanField(default=False)

    # Optional for credits
    college = models.CharField(max_length=255, blank=True)
    degree = models.CharField(max_length=255, blank=True)
    grade = models.PositiveSmallIntegerField(default=0)
    identity = models.CharField(max_length=9, blank=True)
    phone = models.CharField(max_length=13, blank=True)

    # Optional for volunteers
    registered_as_volunteer = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    commentary = models.TextField(null=True)
    shirt_size = models.CharField(max_length=250, choices=SHIRT_SIZE, default='m')
    android_phone = models.BooleanField(default=False)
    rolelist = models.ManyToManyField(VolunteerRole, blank=True, editable=False)


    class Meta:
        unique_together = ('edition', 'email')

    def __str__(self):
        return self.name + " " + self.lastname
    
    def hash(self):
        dhash = hashlib.md5()
        session = { "edition": self.edition.title, "student_id": self.student_id, "identity": self.identity, "email": self.email }
        encoded = json.dumps(session, sort_keys=True).encode()
        dhash.update(encoded)
        return dhash.hexdigest()


class TicketType(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    # valid for this edition
    edition = models.ForeignKey(Edition, on_delete=models.PROTECT)
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
    type = models.ForeignKey(TicketType, on_delete=models.PROTECT)
    attendant = models.OneToOneField(Attendant, on_delete=models.PROTECT)

    secret_key = models.CharField(max_length=16, editable=False)
    signature = models.CharField(max_length=256, blank=True, editable=False)

    def __str__(self):
        return str(self.pk) + " - " + self.attendant.lastname

    def sign(self):
        key = '%s%s%s%s%s' % (
            str(self.time_stamp), str(self.pk), self.attendant.lastname, self.attendant.email, self.secret_key)
        sha1 = hashlib.sha1(key.encode('utf-8'))
        self.signature = sha1.hexdigest()

    def save(self, *args, **kwargs):
        # sign before save
        self.secret_key = get_random_string(16)
        self.sign()
        super(Ticket, self).save(*args, **kwargs)


class CheckIn(models.Model):
    time_stamp = models.DateTimeField()

    attendant = models.ForeignKey(Attendant, on_delete=models.PROTECT)
    session = models.ForeignKey(Session, on_delete=models.PROTECT)
    validator = models.ForeignKey(Validator, on_delete=models.PROTECT )

    class Meta:
        unique_together = ('attendant', 'session')

    def __str__(self):
        return str(self.time_stamp) + " - " + self.attendant.lastname + " - " + self.session.title


class School(models.Model):
    code = models.CharField(max_length=4, primary_key=True)
    name = models.CharField(max_length=255, blank=False)

    def __str__(self):
        return '{}: {}'.format(self.code, self.name)


class Degree(models.Model):
    code = models.CharField(max_length=6, primary_key=True)
    degree = models.CharField(max_length=255, blank=False)
    school = models.ForeignKey(School, on_delete=models.PROTECT)

    def __str__(self):
        return '{}: {}'.format(self.code, self.degree)


