import csv

from django.db.models.functions import Lower

from editions.models import Session
from tickets.models import CheckIn, Attendant


def main():
    # get_all_attendants()
    get_assistance_per_session()


def get_all_attendants():
    checkins = CheckIn.objects.filter(session__edition__year=2017)
    attendants = Attendant.objects \
        .filter(checkin__in=checkins) \
        .distinct() \
        .filter(student=True) \
        .filter(upm_student=True) \
        .order_by(Lower('lastname'))
    write_result('asistentes_2017.csv', attendants)


def get_assistance_per_session():
    writer = csv.writer(open('asis_sesiones_2017.csv', 'w', newline='', encoding='cp1252'), delimiter=';')
    check_all = CheckIn.objects.filter(session__edition__year=2017)
    att_all = Attendant.objects \
        .filter(checkin__in=check_all) \
        .distinct() \
        .filter(student=True) \
        .filter(upm_student=True) \
        .order_by(Lower('lastname'))
    sessions = Session.objects \
        .filter(edition__year=2017) \
        .filter(format__name__in=('Taller', 'Ponencia')) \
        .order_by('start_date')
    writer.writerow([''] + [ses.code for ses in sessions])
    writer.writerow([att.identity for att in att_all])
    for ses in sessions:
        check_ses = CheckIn.objects.filter(session=ses)
        att_ses = Attendant.objects.filter(checkin__in=check_ses)
        writer.writerow([1 if all in att_ses else 0 for all in att_all])


def write_result(file_name, queryset):
    opts = queryset.model._meta
    # the csv writer
    writer = csv.writer(open(file_name, 'w', newline='', encoding='cp1252'), delimiter=';')
    field_names = [field.name for field in opts.fields]
    # Write a first row with header information
    writer.writerow(field_names)
    # Write data rows
    for obj in queryset:
        writer.writerow([getattr(obj, field) for field in field_names])


# Execute main script
main()
