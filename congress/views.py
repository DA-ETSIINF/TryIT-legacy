from django.shortcuts import render

from editions.models import Edition, Session
from tickets.models import Attendant


def home(request):
    return render(request, template_name='congress/home.html')


def activities(request):
    edition = Edition.objects.get(year='2016')
    dates = edition.sessions.datetimes(field_name='start_date', kind='day')

    return render(request, template_name='congress/activities.html', context={
        'edition': edition,
        'dates': dates
    })


def contests(request):
    return render(request, template_name='congress/contests.html')


def workshops(request):
    workshops = Session.objects.filter(edition__year='2016').filter(format__name='Taller')

    return render(request, template_name='congress/workshops.html', context={
        'workshops': workshops
    })


def contact(request):
    return render(request, template_name='congress/contact.html')


def last_editions(request):
    ed_2015 = Edition.objects.get(year='2015')
    ed_2015_dates = ed_2015.sessions.datetimes(field_name='start_date', kind='day')
    ed_2014 = Edition.objects.get(year='2014')
    ed_2014_dates = ed_2014.sessions.datetimes(field_name='start_date', kind='day')
    ed_2013 = Edition.objects.get(year='2013')
    ed_2013_dates = ed_2013.sessions.datetimes(field_name='start_date', kind='day')

    return render(request, template_name='congress/last_editions.html', context={
        'ed_2015': ed_2015,
        'ed_2014': ed_2014,
        'ed_2013': ed_2013,
        'ed_2015_dates': ed_2015_dates,
        'ed_2014_dates': ed_2014_dates,
        'ed_2013_dates': ed_2013_dates
    })


def tickets(request):
    return render(request, template_name='congress/tickets.html', context={
        'colleges': Attendant.COLLEGES
    })
