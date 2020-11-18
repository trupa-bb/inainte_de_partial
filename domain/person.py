class PersonException(Exception):
    def __init__(self, msg=''):
        self._msg = msg

    def __str__(self):
        return self._msg

class PersonValidationException(PersonException):
    def __init__(self, errors):
        self._errors = errors

    @property
    def errors(self):
        return self._errors

    def __str__(self):
        result = ''
        for e in self.errors:
            result += e
            result += '\n'
        return result

class Person:
    def __init__(self, id, name, phone_number):
        self._id = id
        self._name = name
        self._phone_number = phone_number

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def phone_number(self):
        return self._phone_number

    def __str__(self):
        string = '\tID: ' + self.id + ', '
        string += 'Name: ' + self.name.ljust(16) +', '
        string += 'Phone number: ' + self.phone_number.ljust(16)
        return string


class PersonValidator:
    def validate(self, person):
        errors = []
        if len(person.name) < 3:
            errors.append('Name too short!')
        if len(person.id) == 0:
            errors.append('Invalid id!')

        for digit in person.phone_number:
            if digit < '0' or digit > '9':
                errors.append('Invalid phone number!')
                break

        if len(errors) > 0:
            raise PersonValidationException(errors)
