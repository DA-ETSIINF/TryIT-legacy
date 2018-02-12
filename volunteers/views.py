import json

from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.http import HttpResponseNotAllowed
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from volunteers.forms import RegisterVolunteersForm
from volunteers.models import RegisterVolunteers


@csrf_exempt
def submit(request):
    if request.method == 'POST':
        data = request.POST
        form = RegisterVolunteersForm(data)
        if form.is_valid():
            volunteers = RegisterVolunteers()
            volunteers.contact_name = data['contactName'].strip()
            volunteers.company = data.get('company', '').strip()
            volunteers.email = data['email'].strip()
            volunteers.phone = data['phone'].strip()
            volunteers.sponsor = True if data['sponsor'] == 'true' else False

            if volunteers.sponsor:
                volunteers.sponsor_type = data['sponsorType']

            volunteers.sponsor_date = data.get('sponsorDate', '')
            volunteers.type = data['type']
            volunteers.topic = data['topic'].strip()
            volunteers.description = data['description'].strip()

            # File upload
            if 'document' in request.FILES:
                volunteers.document = request.FILES['document']

            volunteers.save()

            return HttpResponse('ok')
        else:
            error = {'id': 2, 'message': 'Error en la validación'}
            return HttpResponseBadRequest(json.dumps(error))
    else:
        return HttpResponseNotAllowed(permitted_methods=['POST'])


def volunteers(request):
    return render(request, template_name='volunteers/volunteers.html')
