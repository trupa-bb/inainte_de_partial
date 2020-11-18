from repository.ActivityRepo import ActivityRepo
from repository.PersonRepo import PersonRepo
from domain.activity import ActivityValidator
from domain.activity import Activity
from datetime import date, time
import random
import string

class ActivityServiceException(Exception):
    def __init__(self, msg=''):
        self._msg = msg

    def __str__(self):
        return self._msg

class ActivityService:
    def __init__(self, activity_repo: ActivityRepo, person_repo: PersonRepo, validator: ActivityValidator):
        self._activity_repo = activity_repo
        self._person_repo = person_repo
        self._validator = validator

    @property
    def activity_repo(self):
        return self._activity_repo

    @property
    def person_repo(self):
        return self._person_repo

    @property
    def validator(self):
        return self._validator

    def check_person_id(self, person_id):
        for person in self._person_repo.persons:
            if person.id == person_id:
                return True
        return False

    def create_activity(self, activity_info, activity_description, persons):
        id, d, t = activity_info.strip().split(',',2)
        id = id.strip()
        day,month,year = d.split('.',2)
        day = int(day.lstrip('0'))
        month = int(month.lstrip('0'))
        year = int(year)
        d = date(year,month,day)
        hour,minute = t.split(':')
        if hour == '00':
            hour = 0
        else:
            hour = int(hour.lstrip('0'))
        if minute == '00':
            minute = 0
        else:
            minute = int(minute.lstrip('0'))
        t = time(hour,minute)
        activity = Activity(id,persons,d,t,activity_description)
        return activity

    def check_for_unique_id(self, id):
        for index in range(len(self.activity_repo.activities)):
            if self.activity_repo.activities[index].activity_id == id:
                return False
        return True

    def check_for_unique_datetime(self, date, time):
        for index in range(len(self.activity_repo.activities)):
            if self.activity_repo.activities[index].date == date and self.activity_repo.activities[index].time == time:
                return False
        return True

    def add_activity(self, activty_info, activity_description, activity_persons):
        '''
        Add a new activity with information from activity_info, activity_description, activity_persons
        :param activty_info: infomarmation avout the id, date and time
        :param activity_description: description of the activity
        :param activity_persons: persons that will perform the activity
        :return:
        '''
        persons = activity_persons.strip().split(',')
        for i in range(len(persons)):
            persons[i] = persons[i].strip()
            if not self.check_person_id(persons[i]):
                raise ActivityServiceException("Person with id " + str(persons[i]) + " not found!")

        activity = self.create_activity(activty_info,activity_description,persons)
        self._validator.validate(activity)
        if self.check_for_unique_id(activity.activity_id) == False:
            raise ActivityServiceException("ID already exists!")
        if not self.check_for_unique_datetime(activity.date,activity.time):
            raise ActivityServiceException("Date and time are used by another activity!")

        self.activity_repo.add_activity(activity)

    def find_by_id(self,id):
        for index in range(len(self.activity_repo.activities)):
            if id == self.activity_repo.activities[index].activity_id:
                return index
        return -1

    def remove_activity(self, activity_id):
        '''
        Remove the activity with activity_id
        :param activity_id: id of the activity to be removed
        :return: -
        '''
        index = self.find_by_id(activity_id)
        if index == -1:
            raise ActivityServiceException("ID not found!")
        self.activity_repo.remove_activity(index)

    def update_activity(self, activity_id, activity_info, activity_description, activity_persons):
        '''
        Update the activity with activity_id with information from activity_info, activity_description, activity_persons
        :param activity_id: id of the activity to be updated
        :param activity_info: info about the new id, date and time
        :param activity_description: new description
        :param activity_persons: persons that will perform the activity
        :return: -
        '''
        index = self.find_by_id(activity_id)
        if index == -1:
            raise ActivityServiceException("ID not found!")

        persons = activity_persons.strip().split(',')
        for i in range(len(persons)):
            persons[i] = persons[i].strip()
            if not self.check_person_id(persons[i]):
                raise ActivityServiceException("Person with id " + str(persons[i]) + " not found!")

        activity = self.create_activity(activity_info, activity_description, persons)
        self._validator.validate(activity)
        if self.check_for_unique_id(activity.activity_id) == False:
            raise ActivityServiceException("ID already exists!")
        if not self.check_for_unique_datetime(activity.date, activity.time):
            raise ActivityServiceException("Date and time are used by another activity!")

        self.activity_repo.update_activity(index,activity)


    def generate_activities(self):
        for i in range(10):
            letters = string.ascii_uppercase
            digits = string.digits

            id = ''.join(random.choice(letters + digits) for i in range(3))
            while self.check_for_unique_id(id) == False:
                id = ''.join(random.choice(letters + digits) for i in range(3))

            length = len(self._person_repo.persons)

            persons_id = []
            hmn = random.randint(1,5)
            for j in range(hmn):
                index = random.randint(0, length - 1)
                while self._person_repo.persons[index].id in persons_id:
                    index = random.randint(0, length - 1)
                persons_id.append(self._person_repo.persons[index].id)

            hmn = random.randint(5, 15)

            description = ''.join(random.choice(string.ascii_lowercase) for i in range(hmn))

            t = time(0,0)
            d = date(1,1,1)
            while not self.check_for_unique_datetime(d,t) or t == time(0,0) and d == date(1,1,1):
                hour = random.randint(0, 23)
                minute = random.randint(0, 59)
                day = random.randint(1, 28)
                month = random.randint(1, 12)
                year = random.randint(2020, 2022)
                d = date(year, month, day)
                t = time(hour, minute)

            activity = Activity(id,persons_id,d,t,description)
            self.activity_repo.add_activity(activity)

