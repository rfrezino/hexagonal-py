from unittest import TestCase

from click.testing import CliRunner

from infrastructure.cli import run_check


class TestCli(TestCase):
    def test_cli_bootstrap_should_return_true(self):
        runner = CliRunner()
        result = runner.invoke(run_check, ['--source_path', '../../../src'])
        assert result.exit_code == 0
        assert result.output == 'Hello Peter!\n'
