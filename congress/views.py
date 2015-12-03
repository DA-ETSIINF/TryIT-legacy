from django.shortcuts import render


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
