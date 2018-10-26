from django.shortcuts import render

# Create your views here.
def attendant_info(request):
    return render(request, template_name='attendance/attendance.html')
