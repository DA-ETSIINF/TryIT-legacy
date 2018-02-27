import json

from tickets.models import School, Degree

colleges = json.load(open('congress/static/congress/angular/colleges.json', encoding='utf8'))

for college in colleges:
    school = School()
    school.code = college['codigo']
    school.name = college['nombre']
    school.save()

    degrees = college['titulaciones']
    for d in degrees:
        degree = Degree()
        degree.code = d['codigo']
        degree.degree = d['nombre']
        degree.school = school
        degree.save()
