import csv

from django.db.models.functions import Lower

from TryIT.settings_global import EDITION_YEAR
from editions.models import Session
from tickets.models import CheckIn, Attendant, School, Degree


def main():
    get_all_attendants()
    get_assistance_per_session()


def get_all_attendants():
    writer = csv.writer(open('asistentes_' + str(EDITION_YEAR) + '.csv', 'w', newline='', encoding='cp1252'),
                        delimiter=';')

    schools = School.objects.all()
    degrees = Degree.objects.all()
    checkins = CheckIn.objects.filter(session__edition__year=EDITION_YEAR)
    attendants = Attendant.objects \
        .filter(checkin__in=checkins) \
        .distinct() \
        .filter(student=True) \
        .filter(upm_student=True) \
        .order_by(Lower('lastname'))

    field_names = ['Nombre', 'Apellidos', 'Email', 'ID Escuela', 'Escuela', 'ID Grado',
                   'Grado', 'Curso', 'DNI', 'Teléfono', 'Nº sesiones', 'Nº talleres']
    writer.writerow(field_names)

    # Write data rows
    for a in attendants:
        checkins_filter = checkins.filter(attendant=a)
        num_sessions = checkins_filter.filter(session__format=1).count()
        num_workshops = checkins_filter.filter(session__format=2).count()

        data = [a.name, a.lastname, a.email, a.college, schools.get(code=a.college).name,
                a.degree, degrees.get(code=a.degree).degree, a.grade, a.identity, a.phone,
                num_sessions, num_workshops]
        writer.writerow(data)


def get_assistance_per_session():
    writer = csv.writer(open('asis_sesiones_' + str(EDITION_YEAR) + '.csv', 'w', newline='', encoding='cp1252'),
                        delimiter=';')
    check_all = CheckIn.objects.filter(session__edition__year=EDITION_YEAR)
    att_all = Attendant.objects \
        .filter(checkin__in=check_all) \
        .distinct() \
        .filter(student=True) \
        .filter(upm_student=True) \
        .order_by(Lower('lastname'))
    sessions = Session.objects \
        .filter(edition__year=EDITION_YEAR) \
        .filter(format__name__in=('Taller', 'Ponencia')) \
        .order_by('start_date')
    writer.writerow([''] + [ses.start_date.strftime('%e - %H:%M') for ses in sessions])
    writer.writerow([att.identity for att in att_all])
    for ses in sessions:
        check_ses = CheckIn.objects.filter(session=ses)
        att_ses = Attendant.objects.filter(checkin__in=check_ses)
        writer.writerow([1 if all in att_ses else 0 for all in att_all])


# Execute main script
main()
