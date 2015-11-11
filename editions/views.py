import json
from editions.models import Edition
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotAllowed
from django.shortcuts import render


def home(request):
    return render(request, template_name='editions/home.html')


@csrf_exempt
def get_editions(request):
    if request.method == 'GET':
        editions = Edition.objects.all()
        return HttpResponse(editions, content_type='application/json')
    else:
        return HttpResponseNotAllowed(permitted_methods='GET')
