import os.path
import pathlib


def get_project_path() -> str:
    return str(pathlib.Path(__file__).resolve().parent.parent)


def get_tests_path() -> str:
    return os.path.join(get_project_path(), 'tests')


def fix_path(path: str) -> str:
    return os.path.normcase(os.path.normpath(path))
