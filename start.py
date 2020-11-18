from ui.UI import UI
from services.ActivityService import ActivityService
from repository.ActivityRepo import ActivityRepo
from domain.activity import ActivityValidator
from services.PersonService import PersonService
from repository.PersonRepo import PersonRepo
from domain.person import PersonValidator

pr = PersonRepo()
pv = PersonValidator()
ps = PersonService(pr,pv)

acr = ActivityRepo()
av = ActivityValidator()
acs = ActivityService(acr,pr,av)

program = UI(ps,acs)

program.start()