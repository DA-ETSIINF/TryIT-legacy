import json

from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.http import HttpResponseNotAllowed
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from TryIT.settings_edition import SPONSOR_TYPE, SPONSOR_DATE, TYPE
from register.forms import RegisterCompanyForm
from register.models import RegisterCompany

from TryIT.url_helper import create_context

@csrf_exempt
def submit(request):
    if request.method == 'POST':
        data = request.POST
        form = RegisterCompanyForm(data)
        if form.is_valid():
            register = RegisterCompany()
            register.contact_name = data['contactName'].strip()
            register.company = data.get('company', '').strip()
            register.email = data['email'].strip()
            register.phone = data['phone'].strip()
            register.sponsor = True if data['sponsor'] == 'true' else False

            if register.sponsor:
                register.sponsor_type = data['sponsorType']

            register.sponsor_date = data.get('sponsorDate', '')
            register.type = data['type']
            register.topic = data['topic'].strip()
            register.description = data['description'].strip()

            # File upload
            if 'document' in request.FILES:
                register.document = request.FILES['document']

            register.save()

            return HttpResponse('ok')
        else:
            error = {'id': 2, 'message': 'Error en la validación'}
            return HttpResponseBadRequest(json.dumps(error))
    else:
        return HttpResponseNotAllowed(permitted_methods=['POST'])


def register(request):
    return render(request, template_name='register/register.html', context=create_context({
        'sponsor_types': SPONSOR_TYPE,
        'dates': SPONSOR_DATE,
        'types': TYPE
    }))