from pathlib import Path

from pytest import FixtureRequest, fixture

from utils.elt_config import QueriesDirectory, check_sql_path_for_blacklist

qdir = QueriesDirectory()


@fixture(
    scope="module",
    params=[x for x in qdir.allchildfiles if x.path.suffix == ".sql"],
    ids=[
        "/".join(x.path.parts[-3:])
        for x in qdir.allchildfiles
        if x.path.suffix == ".sql"
    ],
)
def query_path(request: FixtureRequest) -> Path:
    return request.param


@fixture(scope="module")
def query_text(query_path: Path) -> str:
    return query_path.read_text()


@fixture(scope="module")
def query_name(query_path: Path) -> str:
    return query_path.stem


@fixture(scope="module")
def query_text_upper(query_text: str) -> str:
    return query_text.upper()


def test_query_blacklist(query_path: str) -> None:
    assert not check_sql_path_for_blacklist(query_path), f"{query_path} is blacklisted"
