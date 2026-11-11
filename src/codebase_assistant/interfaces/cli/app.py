import typer

cli = typer.Typer(
    name="codebase-assistant",
    help="AI-powered codebase analysis assistant.",
    invoke_without_command=False,
    no_args_is_help=True,
)


@cli.command()
def version() -> None:
    """Display application version."""
    typer.echo("Codebase Assistant v0.1.0")


@cli.command()
def info() -> None:
    """Display application information."""
    typer.echo("AI-powered codebase analysis assistant.")


if __name__ == "__main__":
    cli()
