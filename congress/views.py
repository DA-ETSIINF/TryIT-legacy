from django.shortcuts import render

from editions.models import Edition


def home(request):
    return render(request, template_name='congress/home.html')


def activities(request):
    return render(request, template_name='congress/activities.html')


def calendar(request):
    return render(request, template_name='congress/calendar.html')


def tickets(request):
    return render(request, template_name='congress/tickets.html')


def contact(request):
    return render(request, template_name='congress/contact.html')


def last_editions(request):
    ed_2015 = Edition.objects.get(year='2015')
    ed_2015_dates = ed_2015.sessions.all().datetimes(field_name='start_date', kind='day')
    ed_2014 = Edition.objects.get(year='2014')
    ed_2014_dates = ed_2014.sessions.all().datetimes(field_name='start_date', kind='day')
    ed_2013 = Edition.objects.get(year='2013')
    ed_2013_dates = ed_2013.sessions.all().datetimes(field_name='start_date', kind='day')

    return render(request, template_name='congress/last_editions.html', context={
        'ed_2015': ed_2015,
        'ed_2014': ed_2014,
        'ed_2013': ed_2013,
        'ed_2015_dates': ed_2015_dates,
        'ed_2014_dates': ed_2014_dates,
        'ed_2013_dates': ed_2013_dates
    })