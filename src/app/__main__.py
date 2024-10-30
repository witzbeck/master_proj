from click import echo, group

from etl import (
    create_schema,
    export_database,
    load_landing_data,
    load_schema,
    queries_dir,
)


@group()
def cli():
    """CLI for building and analyzing the DuckDB database."""
    pass


@cli.command("list-sources-without-targets")
def list_sources_without_targets():
    """List sources without targets."""
    sources = sorted(queries_dir.sources_without_targets)
    for source in sources:
        echo(source)


@cli.command("list-targets-without-sources")
def list_targets_without_sources():
    """List targets without sources."""
    targets = sorted(queries_dir.targets_without_sources)
    for target in targets:
        echo(target)


if __name__ == "__main__":
    cli.add_command(create_schema)
    cli.add_command(load_landing_data)
    cli.add_command(load_schema)
    cli.add_command(export_database)
    cli()
