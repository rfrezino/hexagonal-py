from abc import ABCMeta, abstractclassmethod

from tests.test_projects.wrong_project.domain.person import Person


class PersonRepository(ABCMeta):
    @abstractclassmethod
    def add(self, person: Person):
        ...
