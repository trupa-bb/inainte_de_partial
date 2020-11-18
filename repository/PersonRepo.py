
class PersonRepoException(Exception):
    def __init__(self, msg = ''):
        self._msg = msg

    def __str__(self):
        return self._msg


class PersonRepo:
    def __init__(self):
        self._persons = []

    @property
    def persons(self):
        return self._persons

    def add_person(self, person):
        self.persons.append(person)

    def remove_person(self, index):
        self._persons.pop(index)

    def update_person(self, index, person):
        self._persons[index] = person

