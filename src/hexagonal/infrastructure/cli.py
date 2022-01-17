import logging
import os
import sys
from runpy import run_path

import click

from hexagonal.domain.hexagonal_error import HexagonalError
from hexagonal.domain.hexagonal_layer import HexagonalLayer
from hexagonal.hexagonal_config import hexagonal_config
from hexagonal.services.toml_configuration import TomlConfiguration
from hexagonal.use_cases.check_project_coherence_usecase import CheckProjectCoherenceUseCase, HexagonalCheckResponse
from hexagonal.use_cases.generate_diagram_usecase import GenerateDiagramUseCase


@click.group(help='Options for Hexagonal Coherence Check')
def cli():
    pass


@click.command()
@click.option('--project_path', help='Main project folder.', required=True)
@click.option('--source_path', help='Where main source folder is located.', required=True)
@click.option('--hexagonal_config_file', default='hexagonal_config.py', help="Hexagonal configuration file's name.")
@click.option('--show', default=True, help="Show diagram file upon creation.")
def diagram(project_path, source_path, hexagonal_config_file, show):
    try:
        _process_cli_arguments(project_path=project_path,
                               source_path=source_path,
                               hexagonal_config_file=hexagonal_config_file)

        hexa_diagram = GenerateDiagramUseCase()
        hexa_diagram.execute(project_name='Hexagonal Architecture Diagram', hexagonal_config=hexagonal_config,
                             show=show)
    except Exception as error:
        click.echo(f'Error while generating project\'s diagram: "{error}"')
        exit(1)


@click.command()
@click.option('--project_path', help='Main project folder.', required=True)
@click.option('--source_path', help='Where main source folder is located.', required=True)
@click.option('--hexagonal_config_file', default='hexagonal_config.py', help="Hexagonal configuration file's name.")
def check(project_path: str, source_path: str, hexagonal_config_file: str):
    def _build_response_message() -> str:
        return f'Hexagonal Architecture: Checked a project with {len(response.hexagonal_project.layers)} ' \
               f'hexagonal layers, {len(response.python_files)} python files ' \
               f'and found {len(response.errors)} errors.'

    try:
        _process_cli_arguments(project_path=project_path,
                               source_path=source_path,
                               hexagonal_config_file=hexagonal_config_file)

        checker = CheckProjectCoherenceUseCase(hexagonal_config=hexagonal_config, source_folder=source_path)
        response = checker.check()
        _print_check_response(response)
    except Exception as error:
        logging.error('Error while processing project', exc_info=error)
        click.echo(f'Error while processing project: "{error}"')
        exit(1)

    [_print_error(index, error) for index, error in enumerate(response.errors)]
    if len(response.errors) > 0:
        logging.error(_build_response_message())
        exit(1)

    click.echo(_build_response_message())


def _print_check_response(response: HexagonalCheckResponse):
    hexa_project = response.hexagonal_project
    logging.info(f'Checked information for project: {hexa_project.project_path}')

    for layer in hexa_project.layers:
        logging.info(f'#### Files in layer "{layer.name}"')

        for idx, file in enumerate(layer.python_files):
            logging.info(f' {idx + 1}) File {file.file_full_path}')

    logging.warning(f'#### Files out site of layers')
    for idx, file in enumerate(hexa_project.files_not_in_layers):
        logging.warning(f' {idx + 1}) File {file.file_full_path}')


def _print_error(error_index: int, error: HexagonalError):
    if error_index == 0:
        click.echo('')
        click.echo('#' * 100)
        click.echo('## Hexagonal Architecture errors found:')
        click.echo('## First fix the [ERROR 1] and re-run the check. '
                   'Follows errors can be cascading from it. \n')

    if error.group_inter_dependency:
        click.echo(f'[ERROR {error_index + 1}] Hexagonal Architecture: {error.message}')
        click.echo(f'    Cross modules dependency in layer: {error.inner_layer_name}')
        click.echo(f'    Python file: {error.python_file_problem}')
        click.echo(f'    Outer Module : {error.imported_module_problem}')
        return

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


def _process_cli_arguments(*, project_path: str, source_path: str, hexagonal_config_file: str):
    source_path = os.path.abspath(source_path)

    _validate_project_source_path(source_path=source_path)
    _process_configuration(project_path=project_path,
                           source_path=source_path,
                           hexagonal_config_file=hexagonal_config_file)


def _process_configuration(project_path: str, source_path: str, hexagonal_config_file: str):
    hexagonal_config.clear_layers()
    hexagonal_config.excluded_dirs = []

    if _import_configuration_from_toml_file(project_path=project_path):
        return False

    hexagonal_config_file = source_path + '/' + hexagonal_config_file
    _import_hexagonal_config_file(hexagonal_config_file=hexagonal_config_file)


def _import_configuration_from_toml_file(project_path: str) -> bool:
    toml_file = project_path + '/pyproject.toml'
    if not os.path.isfile(toml_file):
        return False

    config = TomlConfiguration()
    config.load_from_file(file_path=toml_file)

    if not config.has_hexagonalpy_configuration():
        return False

    click.echo(f'Loading configuration from {toml_file}')
    hexagonal_config.excluded_dirs = config.excluded_dirs()

    for layer in config.layers():
        hexagonal_config.add_inner_layer(HexagonalLayer(name=layer['name'],
                                                        directories_groups=layer['directories_groups']))

    return True


def _import_hexagonal_config_file(hexagonal_config_file: str):
    click.echo(f'Checking hexagonal configuration file at: {hexagonal_config_file}')
    if not os.path.isfile(hexagonal_config_file):
        click.echo('Project configuration file not found.')
        exit(1)
    hexagonal_config.clear_layers()
    run_path(hexagonal_config_file)


cli.add_command(check)
cli.add_command(diagram)


def main():
    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', stream=sys.stdout, level=logging.INFO)
    cli()


if __name__ == '__main__':
    main()
