from pytest import FixtureRequest, fixture

from analysis.get_figures import (
    PaperFigure,
    PaperFigures,
    PresentationFigure,
    PresentationFigures,
    ProjectFigure,
    SharedFigures,
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
