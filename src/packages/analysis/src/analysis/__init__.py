from alexlib.core import show_dict

from analysis.get_figures import (
    PaperFigures,
    PresentationFigures,
    ProjectFigure,
    SharedFigures,
)


def get_figure_name_map(
    paper: bool = True, presentation: bool = True
) -> dict[str, ProjectFigure]:
    """Get a map of figure names to figure objects."""
    figmap = {x.value.name: x.value for x in SharedFigures}
    if paper:
        figmap.update({x.value.name: x.value for x in PaperFigures})
    if presentation:
        figmap.update({x.value.name: x.value for x in PresentationFigures})
    return figmap


def get_figure_names_with_funcs() -> list[str]:
    """Get a list of figure names with functions."""
    return [x.name for x in get_figure_name_map().values() if x.func is not None]


if __name__ == "__main__":
    show_dict(get_figure_names_with_funcs())
