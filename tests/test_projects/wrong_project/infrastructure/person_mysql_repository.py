from abc import abstractclassmethod
from tests.test_projects.wrong_project.domain.person import Person
from tests.test_projects.wrong_project.services.person_repository import PersonRepository


class PersonMySqlRepository(PersonRepository):
    @abstractclassmethod
    def add(self, person: Person):
        print(f'Person added {person.name}')
    
    