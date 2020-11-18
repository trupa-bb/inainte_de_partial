from datetime import date, time

class ActivityException(Exception):
    def __init__(self, msg=''):
        self._msg = msg

    def __str__(self):
        return self._msg


class ActivityValidationException(ActivityException):
    def __init__(self, error_list):
        self._errors = error_list

    @property
    def errors(self):
        return self._errors

    def __str__(self):
        result = ''
        for e in self.errors:
            result += e
            result += '\n'
        return result


class Activity:
    def __init__(self, activity_id, person_id, date, time, description):
        self._activity_id = activity_id
        self._person_id = person_id
        self._date = date
        self._time = time
        self._description = description

    @property
    def activity_id(self):
        return self._activity_id

    @property
    def person_id(self):
        return self._person_id

    @property
    def date(self):
        return self._date

    @property
    def time(self):
        return  self._time

    @property
    def description(self):
        return self._description

    def __str__(self):
        string = '\tActivity_ID: ' + self.activity_id + ','
        string += '\tPersons_id: '
        for i in range(len(self.person_id)-1):
            string += self.person_id[i] + ','
        string += self.person_id[len(self.person_id)-1] + ',\n'
        string += '\tDate: ' + str(self.date) + ','
        string += '\tTime: ' + str(self.time) + ','
        string += '\tDescription: ' + str(self.description) + '\n'
        return string

class ActivityValidator:
    def validate(self, activity):
        errors = []
        if len(activity.activity_id) == 0 or activity.activity_id == 0:
            errors.append('Invalid activity id!')
        if len(activity.person_id) == 0 or activity.person_id == 0:
            errors.append('Invalid person id!')
        if len(activity.description) >= 500:
            errors.append('Description too long!')
        if len(activity.description) <= 5:
            errors.append('Description too short!')

        if len(errors) > 0:
            raise ActivityValidationException(errors)


def test_activity():
    a = Activity('5A','23',date(2020,2,3),time(12,30),'This is an event')
    assert a.time == time(12,30)
    assert a.date == date(2020,2,3)
    assert a.activity_id == '5A'
    assert a.person_id == '23'
    assert a.description == 'This is an event'
    av = ActivityValidator()
    try:
        av.validate(a)
    except ActivityValidationException as ave:
        print(ave)


test_activity()