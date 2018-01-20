import json
from json.decoder import JSONDecodeError

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from editions.models import Edition, Session
from tickets.forms import TicketForm
from tickets.functions import sign_validation_request, generate_pdf
from tickets.models import Validator, Ticket, CheckIn, Attendant, TicketType


def home(request):
    return render(request, template_name='tickets/home.html')

@csrf_exempt
def create_ticket(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        form = TicketForm(data)
        if form.is_valid():
            edition = Edition.objects.get(year='2017')
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
            ticket_type = TicketType.objects.get(edition__year='2017', name='General')
            ticket.type = ticket_type
            ticket.attendant = attendant

            # create ticket
            ticket.save()
            generate_pdf(ticket)

            return HttpResponse('ok')
        else:
            error = {'id': 2, 'message': 'Error en la validación'}
            return HttpResponseBadRequest(json.dumps(error))
    else:
        return HttpResponseNotAllowed(permitted_methods=['POST'])


@csrf_exempt
def validate_ticket(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
        except JSONDecodeError:
            return HttpResponseBadRequest('JSON decode error')

        if not isinstance(data, list) or not data:
            return HttpResponseBadRequest('JSON decode error')

        for obj in data:
            # load data
            try:
                session_code = obj['session']
                ticket_id = obj['ticket_id']
                ticket_signature = obj['ticket_signature']
                timestamp = obj['timestamp']
                validator_id = obj['validator_id']
                signature = obj['signature']
            except:
                return HttpResponseBadRequest('JSON decode error')

            # verify validation request
            try:
                validator = Validator.objects.get(pk=validator_id)
                valid_signature = sign_validation_request(
                    session_code,
                    ticket_id,
                    ticket_signature,
                    timestamp,
                    validator_id,
                    validator.secret_key
                )
                if not signature == valid_signature:
                    return HttpResponseBadRequest('Validator signature error')

            except ObjectDoesNotExist:
                return HttpResponseBadRequest('Validator does not exist')

            # verify session exists
            try:
                session = Session.objects.get(code=session_code)
            except ObjectDoesNotExist:
                return HttpResponseBadRequest('Session does not exist')

            # verify ticket exists
            try:
                ticket = Ticket.objects.get(pk=ticket_id)
            except ObjectDoesNotExist:
                return HttpResponseBadRequest('Ticket does not exist')

            # Ignore ticket of past editions
            if ticket.type.edition.year != '2017':
                continue

            original_signature = ticket.signature
            if not original_signature == ticket_signature:
                return HttpResponseBadRequest('False ticket')

            # if the ticket is valid, register the checkin
            checkin = CheckIn()
            checkin.time_stamp = timestamp
            checkin.attendant = ticket.attendant
            checkin.session = session
            checkin.validator = validator
            try:
                checkin.save()
            except:
                # Checkin already registered, ignore
                pass

        return HttpResponse('true')
    else:
        return HttpResponseNotAllowed(permitted_methods=['POST'])
