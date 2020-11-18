from domain.person import PersonValidator,PersonValidationException
from repository.PersonRepo import PersonRepo
from services.PersonService import PersonService,PersonServiceException
from domain.activity import ActivityValidator,ActivityValidationException
from repository.ActivityRepo import ActivityRepo
from services.ActivityService import ActivityService,ActivityServiceException
from datetime import date, time

def test_add_person():
    person_repo = PersonRepo()
    person_validator = PersonValidator()
    person_service = PersonService(person_repo,person_validator)

    person_service.add_person("ABC,Name,0093213132")
    assert person_repo.persons[0].id == 'ABC'
    assert person_repo.persons[0].name == 'Name'
    assert person_repo.persons[0].phone_number == '0093213132'

    person_service.add_person("123 , Name Surname , 0000123123 ")
    assert person_repo.persons[1].id == '123'
    assert person_repo.persons[1].name == 'Name Surname'
    assert person_repo.persons[1].phone_number == '0000123123'

    person_service.add_person("!1A,   Naa   , 321321")
    assert person_repo.persons[2].id == '!1A'
    assert person_repo.persons[2].name == 'Naa'
    assert person_repo.persons[2].phone_number == '321321'

    try:
        person_service.add_person("!1A,   N   , 321321")
        person_service.add_person(",   Name   , 321")
        person_service.add_person("!1A,   Name   , 323211321")
        person_service.add_person("123 , Name Surname , 0000123123 ")
        assert False
    except PersonValidationException:
        pass
    except PersonServiceException:
        pass

def test_add_activity():
    activity_repo = ActivityRepo()
    person_repo = PersonRepo()
    person_validator = PersonValidator()
    person_service = PersonService(person_repo, person_validator)
    activity_validator = ActivityValidator()
    activity_service = ActivityService(activity_repo,person_repo,activity_validator)
    person_service.add_person('123,Name,1322313')
    person_service.add_person('ABC,Name,1322313')
    person_service.add_person('111,Name,1322313')

    activity_service.add_activity("123,12.12.2020,12:00","Description","123")
    assert activity_repo.activities[0].activity_id == '123'
    assert activity_repo.activities[0].date == date(2020,12,12)
    assert activity_repo.activities[0].time == time(12,0)
    assert activity_repo.activities[0].description == "Description"
    assert activity_repo.activities[0].person_id == ["123"]

    activity_service.add_activity("ABC,12.11.2020,13:00", "Description", "123,ABC")
    assert activity_repo.activities[1].activity_id == 'ABC'
    assert activity_repo.activities[1].date == date(2020,11,12)
    assert activity_repo.activities[1].time == time(13, 0)
    assert activity_repo.activities[1].description == "Description"
    assert activity_repo.activities[1].person_id == ["123","ABC"]

    try:
        activity_service.add_activity("123,12.10.2020,13:00", "Description", "123,ABC")
        activity_service.add_activity("321,12.11.2020,13:00", "Description", "123,ABC")
        assert False
    except ActivityServiceException:
        pass
    except ActivityValidationException:
        pass

def test_remove_person():
    person_repo = PersonRepo()
    person_validator = PersonValidator()
    person_service = PersonService(person_repo, person_validator)

    person_service.add_person("ABC,Name,0093213132")
    person_service.add_person("123 , Name Surname , 0000123123 ")
    person_service.add_person("321,   Naa   , 321321")
    person_service.add_person("abc,   Naa   , 321321")
    person_service.add_person("111,   Naa   , 321321")

    person_service.remove_person("123")
    assert person_repo.persons[1].id == '321'
    assert person_repo.persons[1].name == 'Naa'
    assert person_repo.persons[1].phone_number == '321321'
    assert len(person_repo.persons) == 4

    person_service.remove_person("ABC")
    assert person_repo.persons[0].id == '321'
    assert person_repo.persons[0].name == 'Naa'
    assert person_repo.persons[0].phone_number == '321321'
    assert len(person_repo.persons) == 3

    try:
        person_service.remove_person("132")
        person_service.remove_person("123")
        assert False
    except PersonServiceException:
        pass

def test_remove_activity():
    activity_repo = ActivityRepo()
    person_repo = PersonRepo()
    person_validator = PersonValidator()
    person_service = PersonService(person_repo, person_validator)
    activity_validator = ActivityValidator()
    activity_service = ActivityService(activity_repo, person_repo, activity_validator)
    person_service.add_person('123,Name,1322313')
    person_service.add_person('ABC,Name,1322313')
    person_service.add_person('111,Name,1322313')

    activity_service.add_activity("123,12.12.2020,12:00", "Description", "123")
    activity_service.add_activity("ABC,12.10.2020,13:00", "Description", "123,ABC")
    activity_service.add_activity("111,12.09.2020,13:00", "Description", "123,ABC")
    activity_service.add_activity("abc,12.08.2020,13:00", "Description", "123,ABC")

    activity_service.remove_activity('ABC')
    assert activity_repo.activities[1].activity_id == '111'
    assert activity_repo.activities[1].date == date(2020, 9, 12)
    assert activity_repo.activities[1].time == time(13, 0)
    assert activity_repo.activities[1].description == "Description"
    assert activity_repo.activities[1].person_id == ["123","ABC"]
    assert len(activity_repo.activities) == 3

    activity_service.remove_activity("123")
    assert activity_repo.activities[0].activity_id == '111'
    assert activity_repo.activities[0].date == date(2020, 9, 12)
    assert activity_repo.activities[0].time == time(13, 0)
    assert activity_repo.activities[0].description == "Description"
    assert activity_repo.activities[0].person_id == ["123","ABC"]
    assert len(activity_repo.activities) == 2

    try:
        activity_service.remove_activity("ABC")
        activity_service.remove_activity("dsa")
        assert False
    except ActivityServiceException:
        pass

def test_update_person():
    person_repo = PersonRepo()
    person_validator = PersonValidator()
    person_service = PersonService(person_repo, person_validator)

    person_service.add_person("ABC,Name,0093213132")
    person_service.add_person("123 , Name Surname , 0000123123 ")
    person_service.add_person("321,   Naa   , 321321")
    person_service.add_person("abc,   Naa   , 321321")
    person_service.add_person("111,   Naa   , 321321")

    person_service.update_person("123","IDD,New name,1111")
    assert person_repo.persons[1].id == 'IDD'
    assert person_repo.persons[1].name == 'New name'
    assert person_repo.persons[1].phone_number == '1111'

    person_service.update_person("ABC","322,Naa,321321")
    assert person_repo.persons[0].id == '322'
    assert person_repo.persons[0].name == 'Naa'
    assert person_repo.persons[0].phone_number == '321321'

    try:
        person_service.update_person("1321","312321,321321,321312")
        person_service.update_person("test","random,text,test")
        assert False
    except PersonServiceException:
        pass

def test_update_activity():
    activity_repo = ActivityRepo()
    person_repo = PersonRepo()
    person_validator = PersonValidator()
    person_service = PersonService(person_repo, person_validator)
    activity_validator = ActivityValidator()
    activity_service = ActivityService(activity_repo, person_repo, activity_validator)
    person_service.add_person('123,Name,1322313')
    person_service.add_person('ABC,Name,1322313')
    person_service.add_person('111,Name,1322313')

    activity_service.add_activity("123,12.12.2020,12:00", "Description", "123")
    activity_service.add_activity("ABC,12.10.2020,13:00", "Description", "123,ABC")
    activity_service.add_activity("111,12.09.2020,13:00", "Description", "123,ABC")
    activity_service.add_activity("abc,12.08.2020,13:00", "Description", "123,ABC")

    activity_service.update_activity('ABC',"112,12.07.2020,13:00", "Description", "123,ABC")
    assert activity_repo.activities[1].activity_id == '112'
    assert activity_repo.activities[1].date == date(2020, 7, 12)
    assert activity_repo.activities[1].time == time(13, 0)
    assert activity_repo.activities[1].description == "Description"
    assert activity_repo.activities[1].person_id == ["123", "ABC"]

    activity_service.update_activity("111","124,12.12.2012,12:00", "Description", "123")
    assert activity_repo.activities[2].activity_id == '124'
    assert activity_repo.activities[2].date == date(2012, 12, 12)
    assert activity_repo.activities[2].time == time(12, 0)
    assert activity_repo.activities[2].description == "Description"
    assert activity_repo.activities[2].person_id == ["123"]

    try:
        activity_service.update_activity("ABC","111,12.01.2020,13:00", "Description", "123,ABC")
        activity_service.update_activity("ABC","dar,12.12.2020,12:00", "Description", "123,ABC")
        activity_service.update_activity("dsa","dar,12.01.2020,12:00", "Description", "123,ABC")
        assert False
    except ActivityServiceException:
        pass


test_add_person()
test_add_activity()
test_remove_activity()
test_remove_person()
test_update_activity()
test_update_person()