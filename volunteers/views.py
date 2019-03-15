import json
import  datetime
from django.db import transaction
from django.http import HttpResponseNotAllowed, HttpResponseBadRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from TryIT.settings_global import EDITION_YEAR
# from volunteers.models import RegisterVolunteers
from editions.models import Edition
from tickets.models import School, Degree, Attendant
from volunteers.forms import VolunteerForm
from volunteers.models import  VolunteerSchedule

from TryIT.url_helper import create_context


@csrf_exempt
@transaction.atomic
def submit(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        error = VolunteerForm(data).get_error()
        if error != '':
            return HttpResponseBadRequest(json.dumps({'id': 1, 'message': error}))
        attendant = Attendant.objects.filter(identity=data['dni_nie'].strip().upper(), edition__year=EDITION_YEAR)
        if attendant.count() == 0:
            error = {'id': 2, 'message': 'Error, no existe ninguna entrada para tu DNI, consigue una antes de '
                                         'apuntarte para voluntario.'}
            return HttpResponseBadRequest(json.dumps(error))

        if attendant[0].registered_as_volunteer:
            error = {'id': 3, 'message': 'Error, ya estas registrado como voluntario.'}
            return HttpResponseBadRequest(json.dumps(error))

        volunteer = attendant[0]
        volunteer.registered_as_volunteer = True
        volunteer.shirt_size = data['shirt']
        volunteer.android_phone = data['android']

        if 'commentary' in data:
            volunteer.commentary = data['commentary'].strip()

        volunteer.save()

        # Insert schedules
        for schedule in data['schedule_options']:
            volunteer_schedule = VolunteerSchedule()
            volunteer_schedule.schedule = schedule['schedule_type']
            volunteer_schedule.volunteer = volunteer
            # Calculate schedule day
            schedule_day = schedule["date"].split('-')
            volunteer_schedule.day = datetime.date(int(schedule_day[0]), int(schedule_day[1]), int(schedule_day[2]))

            volunteer_schedule.save()

        return HttpResponse()

    else:
        return HttpResponseNotAllowed(permitted_methods=['POST'])


def volunteers(request):
    day_list = []

    edition = Edition.objects.get(year=EDITION_YEAR)
    schedule_list = ['Mañana', 'Tarde']
    school_data = School.objects.all()

    # Convert to JSON
    school_list = [{'code': school.code, 'name': school.name, 'degrees': [
        {'code': degree.code, 'name': degree.degree} for degree in school.degree_set.all()
    ]} for school in school_data]

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
               "schedule_list": schedule_list,
               "school_list": json.dumps(school_list)
               }

    return render(request, 'volunteers/volunteers.html', create_context(context))
