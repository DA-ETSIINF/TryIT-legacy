import hashlib
import json
import os
from io import BytesIO

from django.conf import settings
from django.core.mail import EmailMessage
from reportlab.graphics import renderPDF
from reportlab.graphics.barcode import qr
from reportlab.graphics.shapes import Drawing
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas

from TryIT.settings_global import EDITION_YEAR
from editions.models import Edition


def sign_validation_request(session, ticket_id, ticket_signature, timestamp, validator_id, secret_key):
    key = '%s%s%s%s%s%s' % (session, ticket_id, ticket_signature, timestamp, validator_id, secret_key)
    sha1 = hashlib.sha1(key.encode('utf-8'))
    return sha1.hexdigest()


def generate_pdf(ticket):
    edition = Edition.objects.get(year=EDITION_YEAR)

    width, height = 21 * cm, 7.5 * cm
    attendant_name = ticket.attendant.name + ' ' + ticket.attendant.lastname
    buffer = BytesIO()

    c = canvas.Canvas(buffer, pagesize=(width, height))
    c.setFontSize(26)
    c.drawString(1 * cm, 6.2 * cm, 'Try IT! {}'.format(EDITION_YEAR))
    c.setFontSize(10)
    c.drawString(1 * cm, 5 * cm, 'ETSI Informáticos')
    c.drawString(1 * cm, 4.5 * cm, 'Campus de Montegancedo - Madrid')

    # Headers
    c.setFontSize(8)
    c.drawString(1 * cm, 3.5 * cm, 'Asistente:')
    c.drawString(1 * cm, 2.5 * cm, 'Tipo entrada:')
    c.drawString(1 * cm, 1.5 * cm, 'Fecha:')

    # Data
    c.setFontSize(10)
    c.drawString(1 * cm, 3 * cm, attendant_name)
    c.drawString(1 * cm, 2 * cm, ticket.type.name)

    c.drawString(1 * cm, 1 * cm, '{} - {}'.format(edition.start_date.strftime('%e/%m/%Y'),
                                                  edition.end_date.strftime('%e/%m/%Y')))

    # Logo
    path = os.path.join(settings.STATIC_ROOT, 'congress/img/logo_ticket.png')
    c.drawImage(path, (width / 2 - 2 * cm), (height - 5.7 * cm), 4.4 * cm,
                4 * cm, mask='auto')

    # QR code
    qr_data = {'id': ticket.pk, 'signature': ticket.signature}
    qr_code = qr.QrCodeWidget(json.dumps(qr_data))
    qr_code.barLevel = 'Q'
    qr_code.barWidth = 4 * cm
    qr_code.barHeight = 4 * cm
    d = Drawing(4 * cm, 4 * cm)
    d.add(qr_code)
    renderPDF.draw(d, c, (width - 5 * cm), (height - 5.7 * cm))

    c.showPage()
    c.save()

    pdf = buffer.getvalue()
    buffer.close()

    # Send mail with pdf
    mail(ticket, edition, pdf)


def mail(ticket, edition, pdf):
    email = EmailMessage('Entrada Try IT! {}'.format(EDITION_YEAR),
                         '¡ENHORABUENA! Ya tienes tu entrada para el Congreso Try IT! {}, tendrá lugar del'
                         ' {} al {} de {}.\nEsta entrada deberá conservarse durante todo el evento, ya que será '
                         'pedida en varias ocasiones para el control de asistencia a las charlas. Puedes llevar la '
                         'entrada tanto en formato digital como en formato físico.\n\nSi perteneces a una Escuela de '
                         'la Universidad Politécnica de Madrid recuerda que asistir al evento está reconocido con '
                         'créditos ECTS como se recoge en el Catálogo General de Actividades de la UPM.'
                         .format(EDITION_YEAR, edition.start_date.strftime('%e'),
                                 edition.end_dºate.strftime('%e'), 'Marzo'),
                         'tryit@da.fi.upm.es',
                         [ticket.attendant.email])

    email.attach('ticket_TryIT.pdf', pdf, 'application/pdf')
    email.send()
