from services.PersonService import PersonService
from services.ActivityService import ActivityService
from domain.person import PersonValidationException
from domain.activity import ActivityValidationException
from repository.PersonRepo import PersonRepoException
from repository.ActivityRepo import ActivityRepoException
from services.PersonService import PersonServiceException
from services.ActivityService import ActivityServiceException

class UI:
    def __init__(self, person_service: PersonService, activity_service: ActivityService):
        self._person_service = person_service
        self._activity_service = activity_service
        self.command_dict = {'add': self.add_ui, 'remove': self.remove_ui, 'update': self.update_ui, 'list': self.list_ui}
        self.entity_list = ['person', 'activity']

    def print_menu(self):
        print('Commands available:')
        print('\t-add person/activity')
        print('\t-remove person/activity')
        print('\t-update person/activity')
        print('\t-list person/activity\n')

    def split_command(self,command):
        if command == '':
            return '', ''

        tokens = command.strip().split(' ', 1)
        command_word = tokens[0].lower().strip()
        if len(tokens) == 2:
            command_params = tokens[1].strip()
        else:
            command_params = ''

        return command_word, command_params


    def add_ui(self, params):
        if params in self.entity_list:
            if params == 'person':
                person = input("Insert ID, name, phone number>")
                self._person_service.add_person(person)
            else:
                activity_info = input("Insert ID, date, time>")
                activity_description = input("Insert activity description>")
                activity_persons = input("Insert persons' ID performing the activity>")
                self._activity_service.add_activity(activity_info,activity_description,activity_persons)
        else:
            raise ValueError('Invalid command!')


    def remove_ui(self, params):
        if params in self.entity_list:
            if params == 'person':
                person_id = input("Insert person ID>")
                self._person_service.remove_person(person_id)
            else:
                activity_id =  input("Insert activity ID>")
                self._activity_service.remove_activity(activity_id)
        else:
            raise ValueError('Invalid command!')

    def update_ui(self, params):
        if params in self.entity_list:
            if params == 'person':
                person_id = input("Insert person ID>")
                if self._person_service.find_by_id(person_id) == -1:
                    raise ValueError("ID not found!")
                person = input("Insert ID, name, phone number>")
                self._person_service.update_person(person_id,person)
            else:
                activity_id = input("Insert activity ID>")
                activity_info = input("Insert ID, date, time>")
                activity_description = input("Insert activity description>")
                activity_persons = input("Insert persons' ID performing the activity>")
                self._activity_service.update_activity(activity_id,activity_info,activity_description,activity_persons)
        else:
            raise ValueError('Invalid command!')


    def list_ui(self, params):
        if params in self.entity_list:
            if params == 'person':
                for person in self._person_service.repo.persons:
                    print(str(person))
            else:
                for activity in self._activity_service.activity_repo.activities:
                    print(str(activity))
        else:
            raise ValueError('Invalid command!')


    def start(self):
        done = False
        self._person_service.generate_persons()
        self._activity_service.generate_activities()
        while not done:
            self.print_menu()
            command = input('command>')
            command_word, command_params = self.split_command(command)
            if command_word in self.command_dict:
                try:
                    self.command_dict[command_word](command_params)
                except ValueError as ve:
                    print(ve)
                except PersonValidationException as pve:
                    print(pve)
                except PersonRepoException as pre:
                    print(pre)
                except ActivityRepoException as are:
                    print(are)
                except ActivityValidationException as ave:
                    print(ave)
                except PersonServiceException as pse:
                    print(pse)
                except ActivityServiceException as ase:
                    print(ase)
            elif command_word == 'exit':
                done = True
            else:
                print("Invalid command!\n")

