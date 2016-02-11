import json

import qrcode
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotAllowed
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from editions.models import Edition, Session
from tickets.forms import TicketForm
from tickets.functions import sign_validation_request
from tickets.models import Validator, Ticket, CheckIn, Attendant, TicketType


def home(request):
    return render(request, template_name='tickets/home.html')


@csrf_exempt
def create_ticket(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        form = TicketForm(data)
        if form.is_valid():
            edition = Edition.objects.get(year='2016')
            attendant = Attendant()
            attendant.edition = edition
            attendant.name = data['name'].strip()
            attendant.lastname = data['lastname'].strip()
            attendant.email = data['email'].strip()
            attendant.student = data['student']

            if attendant.student:
                attendant.upm_student = data['upm_student']
                if attendant.upm_student:
                    attendant.college = data['college'].strip()
                    attendant.degree = data['degree'].strip()
                    attendant.grade = data['grade']
                    attendant.identity = data['identity'].upper()
                    attendant.phone = data['phone'].strip()

            # create attendant
            try:
                attendant.save()
            except:
                error = {'id': 1, 'message': 'Email ya registrado'}
                return HttpResponseBadRequest(json.dumps(error))

            ticket = Ticket()
            ticket_type = TicketType.objects.get(edition__year='2016', name='General')
            ticket.type = ticket_type
            ticket.attendant = attendant

            # create ticket
            ticket.save()
            # generate_pdf(ticket)
            mail(ticket)
            return HttpResponse('ok')
        else:
            error = {'id': 2, 'message': 'Error en la validación'}
            return HttpResponseBadRequest(json.dumps(error))
    else:
        return HttpResponseNotAllowed(permitted_methods=['POST'])


def generate_pdf(ticket):
    # Generate QR
    img = qrcode.make('texto de prueba')
    img.save("C:/Users/alvarogtx300/Desktop/qr.png")


def mail(ticket):
    # try:
    send_mail('Mail de prueba Try IT! 2016',
              'Cuerpo del mensaje de prueba',
              'delegacion@da.fi.upm.es',
              [ticket.attendant.email],
              fail_silently=False)

    # except Exception as e:
    #     print("error")
    #     print(e)


@csrf_exempt
def validate_ticket(request):
    if request.method == 'POST':
        time_stamp = timezone.now()

        # session_code
        session_code = request.POST.get('session_code', None)
        if session_code is None:
            return HttpResponseBadRequest('missing parameter: session_code')
        # ticket_id
        ticket_id = request.POST.get('ticket_id', None)
        if ticket_id is None:
            return HttpResponseBadRequest('missing parameter: ticket_id')
        # ticket_signature
        ticket_signature = request.POST.get('ticket_signature', None)
        if ticket_signature is None:
            return HttpResponseBadRequest('missing parameter: ticket_signature')
        # validator_id
        validator_id = request.POST.get('validator_id', None)
        if validator_id is None:
            return HttpResponseBadRequest('missing parameter: validator_id')
        # signature
        signature = request.POST.get('signature', None)
        if signature is None:
            return HttpResponseBadRequest('missing parameter: signature')

        # verify validation request
        try:
            validator = Validator.objects.get(pk=validator_id)
            valid_signature = sign_validation_request(
                session_code,
                ticket_id,
                ticket_signature,
                validator_id,
                validator.secret_key
            )
            if not signature == valid_signature:
                return HttpResponseBadRequest('validator signature error')
        except ObjectDoesNotExist:
            return HttpResponseBadRequest('validator does not exist')

        # verify session exists
        try:
            session = Session.objects.get(code=session_code)
        except ObjectDoesNotExist:
            return HttpResponseBadRequest('session does not exist')
        # verify ticket exists
        try:
            ticket = Ticket.objects.get(pk=ticket_id)
        except ObjectDoesNotExist:
            return HttpResponseBadRequest('ticket does not exist')

        original_signature = ticket.signature
        if not original_signature == ticket_signature:
            return HttpResponseBadRequest('false ticket')

        is_valid = False

        # if the ticket type does not define session or time dependencies, then the ticket is valid.
        if not ticket.type.sessions.all() and not ticket.type.session_formats.all() and ticket.type.start_date is None:
            is_valid = True
        # if the ticket is valid for the selected session
        elif session in ticket.type.sessions.all():
            is_valid = True
        # if the ticket is valid for the selected session format
        elif session.format in ticket.type.session_formats.all():
            is_valid = True
        # if the the valid time of the ticket is not expired
        # TODO validation time delta
        elif ticket.type.start_date < time_stamp < ticket.type.end_date:
            is_valid = True

        # ticket not valid
        else:
            is_valid = False

        # if the ticket is valid, register the check in
        if is_valid:
            check_in = CheckIn()
            check_in.attendant = ticket.attendant
            check_in.session = session
            check_in.save()
            return HttpResponse('ok')
        else:
            return HttpResponseForbidden('ticket invalid')
    else:
        return HttpResponseNotAllowed(permitted_methods=['POST'])
