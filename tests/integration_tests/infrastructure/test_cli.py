from unittest import TestCase

from click.testing import CliRunner

from hexagonal.infrastructure.cli import check
from tests.integration_tests.utils.utils import get_sample_correct_test_project_path, get_sample_wrong_test_project_path
from tests.utils import get_project_path


class TestCli(TestCase):
    def test_cli_bootstrap_should_return_true(self):
        # This tests check the consistency of this on project
        runner = CliRunner()
        result = runner.invoke(check, ['--source_path', get_project_path() + '/src/hexagonal',
                                       '--hexagonal_config_file', 'hexagonal_project_config.py'])

        expected_msg = 'Hexagonal Architecture: Checked a project with 4 hexagonal layers, ' \
                       '25 python files and found 0 errors.'
        self.assertEqual(result.exit_code, 0)
        self.assertIn(expected_msg, result.output)

    def test_cli_run_check_should_return_no_errors_for_correct_project(self):
        # This tests check the consistency of this on project
        runner = CliRunner()
        result = runner.invoke(check, ['--source_path', get_sample_correct_test_project_path()])

        expected_msg = 'Hexagonal Architecture: Checked a project with 4 hexagonal layers, ' \
                       '11 python files and found 0 errors.'
        self.assertEqual(result.exit_code, 0)
        self.assertIn(expected_msg, result.output)

    def test_cli_run_check_should_return_errors_for_wrong_project(self):
        # This tests check the consistency of this on project
        runner = CliRunner()
        result = runner.invoke(check, ['--source_path', get_sample_wrong_test_project_path()])

        self.assertEqual(result.exit_code, 1)
        self.assertIn('Wrong dependency flow. An inner layer is pointing to an outer layer.', result.output)
