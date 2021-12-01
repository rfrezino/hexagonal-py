from tests.utils import get_tests_path


def get_integration_tests_path():
    return get_tests_path() + '/integration_tests'


def get_sample_wrong_test_project_path():
    return get_integration_tests_path() + '/utils/sample_projects/wrong_project'


def get_sample_correct_test_project_path():
    return get_integration_tests_path() + '/utils/sample_projects/correct_project'
