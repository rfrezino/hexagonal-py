import logging
import os
import sys
from runpy import run_path

import click

from domain.hexagonal_error import HexagonalError
from main import hexagonal_config
from use_cases.check_project_sanity_usecase import CheckProjectSanityUseCase
from use_cases.generate_diagram_usecase import GenerateDiagramUseCase


@click.group(help='Options for Hexagonal Sanity Check')
def cli():
    pass


@click.command()
@click.option('--source_path', help='Where main source folder is located.', required=True)
@click.option('--hexagonal_config_file', default='hexagonal_config.py', help="Hexagonal configuration file's name.")
def diagram(source_path, hexagonal_config_file):
    _process_cli_arguments(source_path=source_path, hexagonal_config_file=hexagonal_config_file)

    try:
        hexa_diagram = GenerateDiagramUseCase()
        hexa_diagram.execute(project_name='Hexagonal Architecture Diagram', hexagonal_composition=hexagonal_config,
                             show=True)
    except Exception as error:
        click.echo(f'Error while generating project\'s diagram: "{error}"')
        exit(1)


@click.command()
@click.option('--source_path', help='Where main source folder is located.', required=True)
@click.option('--hexagonal_config_file', default='hexagonal_config.py', help="Hexagonal configuration file's name.")
def run_check(source_path, hexagonal_config_file):
    _process_cli_arguments(source_path=source_path, hexagonal_config_file=hexagonal_config_file)

    try:
        checker = CheckProjectSanityUseCase()
        response = checker.check(composition=hexagonal_config, source_folder=source_path)
    except Exception as error:
        click.echo(f'Error while processing project: "{error}"')
        exit(1)

    [_print_error(index, error) for index, error in enumerate(response.errors)]
    if len(response.errors) > 0:
        logging.error('Hexagonal Architecture: Errors found in dependencies flow.')
        exit(1)

    click.echo('Hexagonal Architecture: No errors found.')


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


def _validate_project_source_path(source_path: str):
    click.echo(f'Checking project at: {source_path}')
    if not os.path.isdir(source_path):
        click.echo('Project folder not found.')
        exit(1)
    sys.path.append(source_path)


def _import_hexagonal_config_file(hexagonal_config_file: str):
    click.echo(f'Checking hexagonal configuration file at: {hexagonal_config_file}')
    if not os.path.isfile(hexagonal_config_file):
        click.echo('Project configuration file not found.')
        exit(1)
    hexagonal_config.clear()
    run_path(hexagonal_config_file)


def _process_cli_arguments(source_path: str, hexagonal_config_file: str):
    source_path = os.path.abspath(source_path)
    hexagonal_config_file = source_path + '/' + hexagonal_config_file

    _validate_project_source_path(source_path=source_path)
    _import_hexagonal_config_file(hexagonal_config_file=hexagonal_config_file)


cli.add_command(run_check)
cli.add_command(diagram)

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', stream=sys.stdout, level=logging.DEBUG)
    cli()
