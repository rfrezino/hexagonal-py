from unittest import TestCase

from click.testing import CliRunner

from infrastructure.cli import run_check


class TestCli(TestCase):
    def test_cli_bootstrap_should_return_true(self):
        # This tests check the consistency of this on project
        runner = CliRunner()
        result = runner.invoke(run_check, ['--source_path', '../../../src'])

        self.assertEqual(result.exit_code, 0)
        self.assertIn('No errors found', result.output)
