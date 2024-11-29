from click import group, option
from tqdm import tqdm

from analysis import get_figure_name_map


@group
def cli():
    """CLI for building and analyzing.
    - the figures
    - the results
    - the abroca
    """
    pass


@cli.command
@option("-n", "--name", default=None, help="Name of the figure to generate.")
@option("-f", "--force", is_flag=True, help="Force generation of existing figures.")
@option(
    "--paper/--no-paper", is_flag=True, default=True, help="Generate paper figures."
)
@option(
    "--presentation/--no-presentation",
    is_flag=True,
    default=True,
    help="Generate presentation figures.",
)
def generate_figures(name: str, force: bool, paper: bool, presentation: bool) -> None:
    if name:
        # Generate only the specified figure
        figure_name_map = get_figure_name_map(paper=True, presentation=True)
        if name not in figure_name_map:
            raise ValueError(f"Figure {name} not found.")
        figure_name_map[name].func()
    else:
        # Generate all figures
        to_gen_figures = {
            name: figure
            for name, figure in get_figure_name_map(
                paper=paper, presentation=presentation
            ).items()
            if figure.func is not None
        }
        for name, figure in tqdm(to_gen_figures.items(), desc="Generating figures"):
            try:
                if figure.exists and not force:
                    print(f"Skipping existing figure: {name}")
                    continue
                figure.func()
                print(f"Generated figure: {name}")
            except Exception as e:
                print(f"Failed to generate figure: {name}")
                print(e)
    print("Done.")


if __name__ == "__main__":
    cli()
