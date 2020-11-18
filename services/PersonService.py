
from domain.person import Person
from repository.PersonRepo import PersonRepo
import random
import string


class PersonServiceException(Exception):
    def __init__(self, msg=''):
        self._msg = msg

    def __str__(self):
        return self._msg


class PersonService:
    def __init__(self, repo : PersonRepo, validator):
        self._repo = repo
        self._validator = validator

    @property
    def repo(self):
        return self._repo

    @property
    def validator(self):
        return self._validator


    def create_person(self, person_string):
        id,name,phone_number = person_string.split(',',2)
        id = id.strip()
        name = name.strip()
        phone_number = phone_number.strip()
        person = Person(id, name, phone_number)
        return person


    def check_for_unique_id(self, id):
        for index in range(len(self.repo.persons)):
            if self.repo.persons[index].id == id:
                return False
        return True


    def add_person(self, person_string):
        '''
        Add a person with information from person_string
        :param person_string: string from where the information is extracted
        :return: -
        '''
        person = self.create_person(person_string)
        self.validator.validate(person)
        if self.check_for_unique_id(person.id):
            self.repo.add_person(person)
        else: raise PersonServiceException('ID already exists!')


    def find_by_id(self, id):
        for index in range(len(self.repo.persons)):
            if self.repo.persons[index].id == id:
                return index
        return -1

    def remove_person(self, person_id):
        '''
        Remove the person with person_id
        :param person_id: id of the person to be deleted
        :return: -
        '''
        index = self.find_by_id(person_id)
        if index == -1:
            raise PersonServiceException("ID not found!")
        self.repo.remove_person(index)


    def update_person(self, person_id, person_string):
        '''
        Update the person with person_id with information from person_string
        :param person_id: id of the person to be updated
        :param person_string: string from where the information is extracted
        :return: -
        '''
        index = self.find_by_id(person_id)
        if index == -1:
            raise PersonServiceException("ID not found!")
        person = self.create_person(person_string)
        self.validator.validate(person)
        if self.check_for_unique_id(person.id) == False:
            raise PersonServiceException("ID already exists!")
        self.repo.update_person(index,person)



    def generate_persons(self):
        for index in range(10):
            person_list = ['Ali Baba', 'Bartolomeu', 'Andreeah', 'Abraham Lincoln', 'Jon Snow', 'Sir Fluffy Paws', 'Malfoy', 'John Cena']

            name = person_list[random.randint(0,6)]

            letters = string.ascii_uppercase
            digits = string.digits

            id = ''.join(random.choice(letters + digits) for i in range(3))
            while self.check_for_unique_id(id) == False:
                id = ''.join(random.choice(letters + digits) for i in range(3))
            phone_number = ''.join(random.choice(digits) for i in range(10))

            person = Person(id,name,phone_number)

            self.repo.add_person(person)
