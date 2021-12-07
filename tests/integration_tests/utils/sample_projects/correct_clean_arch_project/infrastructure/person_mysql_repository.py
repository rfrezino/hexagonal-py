from abc import abstractclassmethod
from tests.integration_tests.utils.sample_projects.correct_clean_arch_project.domain.person import Person
from tests.integration_tests.utils.sample_projects.correct_clean_arch_project.services.person_repository import PersonRepository


class PersonMySqlRepository(PersonRepository):
    @abstractclassmethod
    def add(self, person: Person):
        print(f'Person added {person.name}')
    
    