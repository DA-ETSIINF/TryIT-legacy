from django.conf import settings
from django.core.mail import EmailMessage


def mailValidator(subject, body, to, attachments):
    email = EmailMessage(subject, body, 'tryit@da.fi.upm.es', [to])

    for a in list(attachments.all()):
        email.attach_file(settings.MEDIA_URL + a.file.name)

    email.send()


def mailVolunteer(subject, body, bcc, attachments):
    email = EmailMessage(subject, body, 'tryit@da.fi.upm.es', bcc=bcc)

    for a in list(attachments.all()):
        email.attach_file(settings.MEDIA_URL + a.file.name)

    email.send()
