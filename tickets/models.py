import hashlib

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.crypto import get_random_string

from TryIT.settings_global import EDITION_YEAR
from editions.models import Edition, SessionFormat, Session, Track
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

    # Ects
    ects = models.DecimalField(default=0.00,  validators=[MinValueValidator(0.00), MaxValueValidator(3.00)],
                               max_digits=3, decimal_places=2)

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

    def __init__(self, *args, **kwargs):
        super(Attendant, self).__init__(*args, **kwargs)
        self.__original_active_status = self.active

    def update_ects(self):
        # check if a volunteer has been active, so will increase ects
        if not self.__original_active_status and self.__original_active_status != self.active and self.upm_student:
            self.ects += 1

    def save(self, *args, **kwargs):
        self.update_ects()
        super(Attendant, self).save(*args, **kwargs)


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
    validator = models.ForeignKey(Validator, on_delete=models.PROTECT)

    class Meta:
        unique_together = ('attendant', 'session')

    def __str__(self):
        return str(self.time_stamp) + " - " + self.attendant.lastname + " - " + self.session.title

    def update_ects(self):
        if self.attendant.upm_student:
            track = Track.objects.filter()[1]  # get Principal track, determines talks accounted for ECTS
            number_of_sessions = Session.objects \
                .filter(edition__year=EDITION_YEAR) \
                .filter(track=track).count()

            maximum_ects = 3.0 if self.attendant.active else 2.0

            ects_by_session = round(maximum_ects / number_of_sessions, 2)

            if self.attendant.ects < maximum_ects:
                attendance_ects = self.attendant.ects + ects_by_session # cant reuse self.atteendance.ects, is limited to 3.0
                self.attendant.ects = min(attendance_ects, maximum_ects)
                self.attendant.save()

    def save(self, *args, **kwargs):
        self.update_ects()
        super(CheckIn, self).save(*args, **kwargs)


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


