from tickets.functions import sign_validation_request
from django.utils import timezone
from editions.models import Edition, Session
from attendants.models import Attendant
from tickets.models import Validator, TicketType, Ticket, CheckIn
from django.core.exceptions import ObjectDoesNotExist
from tickets.forms import TicketForm
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotAllowed
from django.shortcuts import render


def home(request):
    return render(request, template_name='tickets/home.html')


@csrf_exempt
def create_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            edition = Edition.objects.get(year=form.cleaned_data['edition'])
            attendant = Attendant()
            attendant.edition = edition
            attendant.name = form.cleaned_data['name']
            attendant.email = form.cleaned_data['email']
            attendant.company = form.cleaned_data['company']
            attendant.university = form.cleaned_data['university']
            attendant.faculty = form.cleaned_data['faculty']
            attendant.matriculation_number = form.cleaned_data['matriculation_number']
            # create attendant
            try:
                attendant.save()
            except:
                # TODO check attendant creation errors
                return HttpResponseBadRequest('email registered')

            ticket_type = TicketType.objects.get(pk=form.cleaned_data['ticket_type'])
            ticket = Ticket()
            ticket.attendant = attendant
            ticket.type = ticket_type
            # create ticket
            ticket.save()
            return HttpResponse('ok')
        else:
            return HttpResponseBadRequest('validation error: ' + str(form.errors))
    else:
        return HttpResponseNotAllowed(permitted_methods=['POST'])


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
