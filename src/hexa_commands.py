from src.hexa_diagram import generate_diagram
from src.hexa_sanity_check import HexagonalError, HexagonalSanityCheck


def print_error(error_index: int, error: HexagonalError):
    if error_index == 0:
        print('')
        print('#' * 100)
        print('## Hexagonal Architecture errors found:')
        print('## First fix the [ERROR 1] and re-run the check. '
              'Follows errors can be cascading from it. \n')

    print(f'[ERROR {error_index + 1}] Hexagonal Architecture: {error.message}')
    print(f'    Wrong flow: {error.inner_layer_name} -> {error.outer_layer_name}')
    print(f'    Python file: {error.python_file_problem}')
    print(f'    Outer Module : {error.imported_module_problem}')


def run_command(command: str):
    if command == 'diagram':
        generate_diagram()
    elif command == 'check':
        checker = HexagonalSanityCheck()
        errors = checker.check('src/')

        [print_error(index, error) for index, error in enumerate(errors)]
        if len(errors) > 0:
            raise Exception('Hexagonal Architecture: Errors found in dependencies flow')

        print('Hexagonal Architecture: No errors found')
    else:
        print(f'Command "{command}" not found. Did you mean `diagram` or `check`?')
