import datetime

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from TryIT.settings_global import EDITION_YEAR
# from volunteers.models import RegisterVolunteers
from editions.models import Edition
from volunteers.models import Schedule


@csrf_exempt
def submit(request):
    # if request.method == 'POST':
    #     data = request.POST
    #     form = RegisterVolunteersForm(data)
    #     if form.is_valid():
    #         volunteers = RegisterVolunteers()
    #         volunteers.contact_name = data['contactName'].strip()
    #         volunteers.company = data.get('company', '').strip()
    #         volunteers.email = data['email'].strip()
    #         volunteers.phone = data['phone'].strip()
    #         volunteers.sponsor = True if data['sponsor'] == 'true' else False
    #
    #         if volunteers.sponsor:
    #             volunteers.sponsor_type = data['sponsorType']
    #
    #         volunteers.sponsor_date = data.get('sponsorDate', '')
    #         volunteers.type = data['type']
    #         volunteers.topic = data['topic'].strip()
    #         volunteers.description = data['description'].strip()
    #
    #         # File upload
    #         if 'document' in request.FILES:
    #             volunteers.document = request.FILES['document']
    #
    #         volunteers.save()
    #
    #         return HttpResponse('ok')
    #     else:
    #         error = {'id': 2, 'message': 'Error en la validación'}
    #         return HttpResponseBadRequest(json.dumps(error))
    # else:
    #     return HttpResponseNotAllowed(permitted_methods=['POST'])
    pass


def volunteers(request):
    day_list = []

    edition = Edition.objects.get(year=EDITION_YEAR)
    schedule_list = Schedule.objects.filter(edition=edition)

    start_date = edition.start_date
    end_date = edition.end_date
    # Calculate de difference between two dates. The difference between 26 and 23 is 3, we need to add 1
    ndays = int((end_date - start_date).days)

    # calculate days of event, it will exclude weekends
    for day in range(0, ndays + 1):
        day_event = start_date + datetime.timedelta(days=day)
        # .weekday returns a number between 0 to 6. If the dif  :is less than 0, the day is saturday or sunday
        if int(day_event.weekday()) - 5 < 0:
            day_list.append(day_event)

    context = {"day_list": day_list,
               "schedule_list": schedule_list
               }

    return render(request, 'volunteers/volunteers.html', context)
