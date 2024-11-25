from pathlib import Path
from unittest.mock import MagicMock, patch

from pytest import FixtureRequest, fixture, mark

from analysis.get_figures import (
    PaperFigure,
    PaperFigures,
    PresentationFigure,
    PresentationFigures,
    ProjectFigure,
    SharedFigures,
    generate_figures,
)


@fixture(scope="module", params=[x.value for x in SharedFigures])
def shared_figure(request: FixtureRequest) -> ProjectFigure:
    return request.param


@fixture(scope="module", params=[x.value for x in PaperFigures])
def paper_figure(request: FixtureRequest) -> PaperFigure:
    return request.param


@fixture(scope="module", params=[x.value for x in PresentationFigures])
def presentation_figure(request: FixtureRequest) -> PresentationFigure:
    return request.param


def test_shared_figure_is_project_figure(shared_figure: ProjectFigure):
    assert isinstance(shared_figure, ProjectFigure), f"{shared_figure.name}"


def test_paper_figure_is_paper_figure(paper_figure: PaperFigure):
    assert isinstance(paper_figure, PaperFigure), f"{paper_figure.name}"


def test_presentation_figure_is_presentation_figure(
    presentation_figure: PresentationFigure,
):
    assert isinstance(
        presentation_figure, PresentationFigure
    ), f"{presentation_figure.name}"


def test_paper_figure_is_project_figure(paper_figure: PaperFigure):
    assert issubclass(paper_figure.__class__, ProjectFigure), f"{paper_figure.name}"


def test_presentation_figure_is_project_figure(presentation_figure: PresentationFigure):
    assert issubclass(
        presentation_figure.__class__, ProjectFigure
    ), f"{presentation_figure.name}"


def test_shared_figure_path_exists(shared_figure: ProjectFigure):
    assert shared_figure.exists, f"{shared_figure.name}"


def test_paper_figure_path_exists(paper_figure: PaperFigure):
    assert paper_figure.exists, f"{paper_figure.name}"


def test_presentation_figure_path_exists(presentation_figure: PresentationFigure):
    assert presentation_figure.exists, f"{presentation_figure.name}"


@fixture(scope="module", params=[True, False])
def include_paper(request: FixtureRequest) -> bool:
    return request.param


@fixture(scope="module", params=[True, False])
def include_presentation(request: FixtureRequest) -> bool:
    return request.param


@fixture(scope="module", params=[True, False])
def overwrite(request: FixtureRequest) -> bool:
    return request.param


@fixture(scope="module")
def n_shared_figures() -> int:
    return len(SharedFigures)


@fixture(scope="module")
def n_paper_figures() -> int:
    return len(PaperFigures)


@fixture(scope="module")
def n_presentation_figures() -> int:
    return len(PresentationFigures)


@mark.slow
def test_generate_figures(
    include_paper: bool,
    include_presentation: bool,
    overwrite: bool,
    n_shared_figures: int,
    n_paper_figures: int,
    n_presentation_figures: int,
):
    with (
        patch("analysis.get_figures.read_parquet", return_value=MagicMock()),
        patch("analysis.get_figures.open_pdf", return_value=MagicMock()),
        patch("analysis.get_figures.scatterplot"),
        patch("analysis.get_figures.histplot"),
        patch("analysis.get_figures.savefig"),
        patch("analysis.get_figures.ProjectFigure.func", return_value=MagicMock()),
        patch(
            "analysis.get_figures.ProjectFigure.filepath", return_value=Path(__file__)
        ),
    ):
        figures_to_generate = generate_figures(
            include_paper=include_paper,
            include_presentation=include_presentation,
            overwrite=overwrite,
        )

        nfigs = len(figures_to_generate)
        assert nfigs > 0 or not overwrite
        assert all(fig.exists for fig in figures_to_generate)

        expected_max_count = n_shared_figures
        if include_paper:
            expected_max_count += n_paper_figures
        if include_presentation:
            expected_max_count += n_presentation_figures
        assert nfigs <= expected_max_count
