# from volunteers.models import RegisterVolunteers
import re


class VolunteerForm():
    def __init__(self, data):
        self.name = data.get('name', '')
        self.lastname = data.get('lastname', '')
        self.email = data.get('email', '')
        self.expedient = data.get('expedient', '')
        self.phone = data.get('phone', '')

        self.college = data.get('college', '')
        self.degree = data.get('degree', '')

        self.android = data.get('android', '')
        self.shirt = data.get('shirt', '')

        self.schedule = data.get('schedule', {})

    def is_valid(self):
        if self.name == '' or self.lastname == '' or self.email == '' or self.expedient == '' or self.phone == '':
            return False

        if self.college == '' or self.degree == '':
            return False

        if self.android == '' or self.shirt == '' or not isinstance(self.android, bool):
            return False

        # Check schedule
        for s in self.schedule:
            if not re.match(r'^s\d\d_\d+$', s):
                return False

        return True
