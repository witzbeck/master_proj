from click import echo, group, option

from etl.elt_config import QueriesDirectory, transform_data
from etl.load_dataset import load_dataset


@group()
def cli():
    """CLI for building and analyzing the DuckDB database."""
    pass


@cli.command
@option("-f", "--force/--no-force", default=False, help="Force download and extraction")
@option("-c", "--cleanup/--no-cleanup", default=True, help="Cleanup after extraction")
@option("-v", "--verbose/--no-verbose", default=True, help="Verbose output")
def load(force: bool, cleanup: bool, verbose: bool) -> None:
    """Download and extract the dataset."""
    load_dataset(force=force, cleanup=cleanup)


@cli.command
@option("--replace/--no-replace", default=True, help="Replace existing tables/views")
def transform(replace):
    """Build the database."""
    transform_data(replace=replace)


@cli.command
def list_sources_without_targets():
    """List sources without targets."""
    qdir = QueriesDirectory()
    sources = sorted(qdir.sources_without_targets)
    for source in sources:
        echo(source)


@cli.command
def list_targets_without_sources():
    """List targets without sources."""
    qdir = QueriesDirectory()
    targets = sorted(qdir.targets_without_sources)
    for target in targets:
        echo(target)


@cli.command
@option("--name", default=None, help="Name of the figure to generate.")
def generate_figures(name):
    if name:
        # Generate only the specified figure
        generate_figure(name)
    else:
        # Generate all figures
        generate_all_figures()


def generate_figure(name):
    # Code to generate the specified figure
    print(f"Generating figure: {name}")
    # Add your figure generation logic here


def generate_all_figures():
    # Code to generate all figures
    print("Generating all figures")
    # Add your figure generation logic here


if __name__ == "__main__":
    generate_figures()


if __name__ == "__main__":
    cli()
