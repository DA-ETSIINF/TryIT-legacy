import re


class TicketForm():
    def __init__(self, data):
        self.dni_nie = data.get('identity', '' )

    def get_error(self):
        if self.dni_nie == '':
            return 'Error en el DNI'
        return ''