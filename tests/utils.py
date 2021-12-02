def get_project_path() -> str:
    return __file__.split('/tests')[0]


def get_tests_path() -> str:
    return get_project_path() + '/tests'
