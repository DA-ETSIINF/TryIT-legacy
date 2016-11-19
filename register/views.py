import json

from register.forms import RegisterCompanyForm
from register.models import RegisterCompany


def submit(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        form = RegisterCompanyForm(data)
        if form.is_valid():
            register = RegisterCompany()
            register.contact_name = data['name'].strip()
            register.company = data['company'].strip()
            register.email = data['email'].strip()
            register.phone = data['phone'].strip()
            register.sponsor = data['sponsor']

            if register.sponsor:
                register.sponsor_type = data['sponsor_type']
                register.sponsor_date = data['sponsor_date']

            register.description = data['topic']
            register.description = data['description'].trim()

            # File upload
            register.description = request.FILES['doc']
            request.save()

        return None
    return None
