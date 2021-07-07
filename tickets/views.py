import json
from datetime import datetime
from json.decoder import JSONDecodeError

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from TryIT.settings_global import EDITION_YEAR
from editions.models import Edition, Session
from tickets.forms import TicketForm
from tickets.functions import sign_validation_request, generate_pdf, mail
from tickets.logic import sendData
from tickets.models import Validator, Ticket, CheckIn, Attendant, TicketType

from TryIT.url_helper import create_context


def tickets(request):
    return render(request, template_name='tickets/tickets.html', context=create_context())


@csrf_exempt
def create_ticket(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        form = TicketForm(data)
        error = form.get_error()
        if error != '':
            error = {'id': 2, 'message': error}
            return HttpResponseBadRequest(json.dumps(error))

        edition = Edition.objects.get(year=EDITION_YEAR)
        attendant = Attendant()
        attendant.edition = edition
        attendant.name = data['name'].strip()
        attendant.lastname = data['lastname'].strip()
        attendant.email = data['email'].strip()
        attendant.is_student = data['student']
        attendant.identity = data['identity'].strip().upper()

        # you know covid bruh???
        # attendant.print_accreditation = data["toPrint"]
        attendant.print_accreditation = False

        # check if an attendant with that DNI already exists
        if Attendant.objects.filter(identity=attendant.identity,  edition=edition).count() != 0:
            error = {'id': 3, 'message': 'DNI ya registrado'}
            return HttpResponseBadRequest(json.dumps(error))

        if attendant.is_student:
            attendant.is_upm_student = data['is_upm_student']
            if attendant.is_upm_student:
                attendant.student_id = data['student_id'].strip().lower()
                attendant.college = data['college'].strip()
                attendant.degree = data['degree'].strip()
                attendant.grade = data['grade']
                attendant.phone = data['phone'].strip()

        # create attendant
        try:
            attendant.save()
        except:
            error = {'id': 1, 'message': 'Email ya registrado'}
            return HttpResponseBadRequest(json.dumps(error))

        ticket = Ticket()
        ticket_type = TicketType.objects.get(edition__year=EDITION_YEAR, name='General')
        ticket.type = ticket_type
        ticket.attendant = attendant
        
        edition = Edition.objects.get(year=EDITION_YEAR)

        # create ticket
        ticket.save()
        pdf = generate_pdf(ticket, edition)

        # Send mail with pdf
        mail(ticket, edition, pdf, attendant.is_upm_student and attendant.is_student)
        return HttpResponse('ok')
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
                session_id = obj['session']
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
                    session_id,
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
                session = Session.objects.get(id=session_id)
            except ObjectDoesNotExist:
                return HttpResponseBadRequest('Session does not exist')

            # verify ticket exists
            try:
                ticket = Ticket.objects.get(pk=ticket_id)
            except ObjectDoesNotExist:
                return HttpResponseBadRequest('Ticket does not exist')

            # Ignore ticket of past editions
            if ticket.type.edition.year != str(EDITION_YEAR):
                continue

            original_signature = ticket.signature
            if not original_signature == ticket_signature:
                return HttpResponseBadRequest('False ticket')

            # if the ticket is valid, register the checkin
            checkin = CheckIn()
            checkin.time_stamp = datetime.fromtimestamp(timestamp / 1e3)
            checkin.attendant = ticket.attendant
            checkin.session = session
            checkin.validator = validator
            try:
                checkin.save(ticket)
            except:
                # Checkin already registered, ignore
                pass

            try:
                #sendData(ticket.signature)
                pass
            except:
                pass

        return HttpResponse('true')
    else:
        return HttpResponseNotAllowed(permitted_methods=['POST'])
