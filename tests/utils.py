def get_project_path() -> str:
    return __file__.split('/tests')[0]


def get_sample_wrong_test_project_path():
    return get_project_path() + '/tests/test_projects/wrong_project'


def get_sample_correct_test_project_path():
    return get_project_path() + '/tests/test_projects/correct_project'
