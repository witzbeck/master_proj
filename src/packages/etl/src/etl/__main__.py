from click import echo, group, option

from .elt_config import QueriesDirectory, main


@group()
def cli():
    """CLI for building and analyzing the DuckDB database."""
    pass


@cli.command()
@option("--replace/--no-replace", default=True, help="Replace existing tables/views")
def build(replace):
    """Build the database."""
    main(replace=replace)


@cli.command("list-sources-without-targets")
def list_sources_without_targets():
    """List sources without targets."""
    qdir = QueriesDirectory()
    sources = sorted(qdir.sources_without_targets)
    for source in sources:
        echo(source)


@cli.command("list-targets-without-sources")
def list_targets_without_sources():
    """List targets without sources."""
    qdir = QueriesDirectory()
    targets = sorted(qdir.targets_without_sources)
    for target in targets:
        echo(target)


if __name__ == "__main__":
    cli()
