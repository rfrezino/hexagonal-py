import importlib.util
import logging
import os
import sys

import click

from domain.hexagonal_error import HexagonalError
from services.hexagonal_composition import HexagonalComposition
from use_cases.check_project_sanity_usecase import CheckProjectSanityUseCase
from use_cases.generate_diagram_usecase import GenerateDiagramUseCase

hexagonal_composition = HexagonalComposition()


def _print_error(error_index: int, error: HexagonalError):
    if error_index == 0:
        click.echo('')
        click.echo('#' * 100)
        click.echo('## Hexagonal Architecture errors found:')
        click.echo('## First fix the [ERROR 1] and re-run the check. '
                   'Follows errors can be cascading from it. \n')

    click.echo(f'[ERROR {error_index + 1}] Hexagonal Architecture: {error.message}')
    click.echo(f'    Wrong flow: {error.inner_layer_name} -> {error.outer_layer_name}')
    click.echo(f'    Python file: {error.python_file_problem}')
    click.echo(f'    Outer Module : {error.imported_module_problem}')


@click.group(help='Options for Hexagonal Sanity Check')
def cli():
    pass


def _load_module(file_name, module_name):
    spec = importlib.util.spec_from_file_location(module_name, file_name)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


@click.command()
@click.option('--config_file', default='hexagonal_config.py', help='Where is Hexagonal config is set.')
def diagram(config_file: str):
    diagram = GenerateDiagramUseCase()

    # importlib.import_module(config_file, package='./src/')

    my_module = _load_module(config_file, 'src')

    diagram.execute(project_name='Hexagonal Architecture Diagram',
                    hexagonal_composition=hexagonal_composition)


@click.command()
@click.option('--source_path', default='src/', help='Where main source folder is located.', required=True)
def run_check(source_path):
    source_path = os.path.abspath(source_path)
    click.echo(f'Checking project at: {source_path}')

    if not os.path.isdir(source_path):
        click.echo('Project folder not found.')
        exit(1)

    sys.path.append(source_path)

    try:
        checker = CheckProjectSanityUseCase()
        response = checker.check(composition=hexagonal_composition, source_folder=source_path)
    except Exception as error:
        click.echo(f'Error while processing project: "{error}"')
        exit(1)

    [_print_error(index, error) for index, error in enumerate(response.errors)]
    if len(response.errors) > 0:
        raise Exception('Hexagonal Architecture: Errors found in dependencies flow.')

    click.echo('Hexagonal Architecture: No errors found.')


cli.add_command(run_check)
cli.add_command(diagram)

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', stream=sys.stdout, level=logging.DEBUG)
    cli()
