import hashlib

from django.db import models
from django.utils.crypto import get_random_string

from editions.models import Edition, SessionFormat, Session


class Validator(models.Model):
    name = models.CharField(max_length=255)
    secret_key = models.CharField(max_length=16, editable=False)

    def __str__(self):
        return str(self.pk) + " - " + self.name

    def save(self, *args, **kwargs):
        # generate key before save
        self.secret_key = get_random_string(16)
        super(Validator, self).save(*args, **kwargs)


class Attendant(models.Model):
    COLLEGES = (
        ('etsiinf', 'E.T.S. de Ingenieros Informáticos'),
        ('arquitectura', 'E.T.S. de Arquitectura'),
        ('edificacion', 'E.T.S. de Edificación'),
        ('etsiae', 'E.T.S. de Ingeniería Aeronaútica y del Espacio'),
        ('agronomos', 'E.T.S. de Ingeniería Agronómica, Alimentaria y de Biosistemas'),
        ('montes', 'E.T.S. de Ingeniería de Montes, Forestal y del Medio Natural'),
        ('caminos', 'E.T.S. de Ingenieros de Caminos, Canales y Puertos'),
        ('etsit', 'E.T.S. de Ingenieros de Telecomunicación'),
        ('etsin', 'E.T.S. de Ingenieros Navales'),
        ('inef', 'Facultad de Ciencias de la Actividad Física y del Deporte (INEF)'),
        ('civil', 'E.T.S. de Ingeniería Civil'),
        ('etsidi', 'E.T.S. de Ingeniería y Diseño Industrial'),
        ('minas', 'E.T.S. de Ingenieros de Minas y Energía'),
        ('etsii', 'E.T.S. de Ingenieros Industriales'),
        ('etsisi', 'E.T.S. de Ingeniería de Sistemas Informáticos'),
        ('euitt', 'E.T.S. de Ingeniería y Sistemas de Telecomunicación'),
        ('topografia', 'E.T.S. de Ingenieros en Topografía, Geodesia y Cartografía')
    )

    edition = models.ForeignKey(Edition)
    name = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    email = models.EmailField()
    student = models.BooleanField(default=False)
    upm_student = models.BooleanField(default=False)

    # Optional for credits
    college = models.CharField(max_length=255, blank=True, choices=COLLEGES)
    degree = models.CharField(max_length=255, blank=True)
    grade = models.PositiveSmallIntegerField(default=0)
    identity = models.CharField(max_length=9, blank=True)
    phone = models.CharField(max_length=13, blank=True)

    class Meta:
        unique_together = ('edition', 'email')

    def __str__(self):
        return self.name + " " + self.lastname


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
    attendant = models.OneToOneField(Attendant)

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
    time_stamp = models.DateTimeField(auto_now_add=True)

    attendant = models.ForeignKey(Attendant)
    session = models.ForeignKey(Session)
    validator = models.ForeignKey(Validator)

    class Meta:
        unique_together = ('attendant', 'session')

    def __str__(self):
        return str(self.time_stamp) + " - " + self.attendant.lastname + " - " + self.session.title
