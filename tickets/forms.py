import re


class TicketForm():
    def __init__(self, data):
        self.name = data.get('name', '')
        self.lastname = data.get('lastname', '')
        self.email = data.get('email', '')
        self.student = data.get('student', False)
        self.upm_student = data.get('upm_student', False)

        self.college = data.get('college', '')
        self.degree = data.get('degree', '')
        self.grade = data.get('grade', 0)
        self.identity = data.get('identity', '')
        self.phone = data.get('phone', '')

    def is_valid(self):
        if self.name == '' or self.lastname == '' or self.email == '':
            return False

        if isinstance(self.student, bool) and self.student:
            if isinstance(self.student, bool) and self.upm_student:
                if self.college == '' or self.degree == '' or self.phone == '':
                    return False
                elif isinstance(self.grade, int) and 1 <= self.grade <= 4:
                    if re.match(r'^[x-z]{1}[-]?\d{7}[-]?[a-z]{1}$|^\d{8}[-]?[a-z]{1}$', self.identity,
                                re.IGNORECASE):
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return True
        else:
            return True
