from typer.testing import CliRunner

from codebase_assistant.interfaces.cli.app import cli

runner = CliRunner()


def test_version_command() -> None:
    result = runner.invoke(cli, ["version"])

    assert result.exit_code == 0
    assert result.stdout.strip() == "Codebase Assistant v0.1.0"


def test_info_command() -> None:
    result = runner.invoke(cli, ["info"])

    assert result.exit_code == 0
    assert result.stdout.strip() == "AI-powered codebase analysis assistant."
