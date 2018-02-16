import json
import datetime

from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.http import HttpResponseNotAllowed
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from volunteers.forms import RegisterVolunteersForm
from volunteers.models import RegisterVolunteers
from editions.models import Edition



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
    daynumber = [ []]
    dayname = [ ]

    start_date = Edition.objects.latest('pk').start_date
    end_date = Edition.objects.latest('pk').end_date
    #Calculate de difference between two dates. The difference between 26 and 23 is 3, we need to add 1
    ndays = int(( end_date - start_date).days) + 1
    # calculate days of event, it will exclude weekends
    for day in range(0, ndays):
        dayevent = start_date + datetime.timedelta(days=day)
    # .weekday returns a number between 0 to 6. If the dif  :is less than 0, the day is saturday or sunday
        if int(dayevent.weekday()) - 5 < 0:
            #context.update({ ("day"+ str(day)) : str(dayevent.day) + "-" + str(dayevent.month) })
            daynumber += [str(dayevent.day) + "-" + str(dayevent.month), str(dayevent.strftime("%A"))]
            dayname += []
    context = {"daynumber": daynumber,
               "dayname": dayname
               }

    return render(request, 'volunteers/volunteers.html', context)

