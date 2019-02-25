from django.core.mail import EmailMessage
from TryIT.settings_global import EDITION_YEAR


def mail(date, eventname, attendant, place):
    email = EmailMessage('Registro para el Try IT! {}'.format(EDITION_YEAR),
                         '¡ENHORABUENA! Ya tienes tu entrada para el {}, tendrá lugar el' 
                         ' {} en {}.'.format(eventname, str(date), place),
                         'tryit@da.fi.upm.es',
                         [attendant.email])

    email.send()
