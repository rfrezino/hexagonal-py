from abc import ABCMeta, abstractclassmethod

from tests.unit_tests.use_cases.test_projects.wrong_project.domain.person import Person


class PersonRepository(ABCMeta):
    @abstractclassmethod
    def add(self, person: Person):
        ...
