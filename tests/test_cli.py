# -*- coding: utf-8 -*-

"""
test_cli
----------------------------------

Tests for `cli` module.
"""

# thirdparty libraies
import pytest

# This package
from ar_too import cli

class TestCli:
    def test_cli(self, cli_runner):
        result = cli_runner.invoke(cli.cli, ['--help'])
        assert result.exit_code == 0
        assert result.output.startswith('Usage:')

