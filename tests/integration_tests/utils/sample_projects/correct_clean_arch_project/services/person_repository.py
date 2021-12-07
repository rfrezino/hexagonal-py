from abc import ABCMeta, abstractclassmethod

from tests.integration_tests.utils.sample_projects.correct_clean_arch_project.domain.person import Person


class PersonRepository(ABCMeta):
    @abstractclassmethod
    def add(self, person: Person):
        ...
