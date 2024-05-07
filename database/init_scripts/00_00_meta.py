from dataclasses import dataclass, field
from functools import partial
from pathlib import Path

this = Path(__file__)
here = this.parent


def paths_factory(path: Path, pattern: str) -> list[Path]:
    return list(path.glob(pattern))


sqlpaths_factory = partial(paths_factory, pattern="*.sql", path=here)


@dataclass(slots=True)
class PathGroup:
    paths: list[Path] = field(default_factory=paths_factory)

    def __post_init__(self) -> None:
        self.paths = self.paths()

    def __repr__(self) -> str:
        return f"[{here.name}]{self.__class__.__name__}({self.count})"

    @property
    def count(self) -> int:
        return len(self.paths)

    @staticmethod
    def _compare_branch_names(in_set: set, in_list: list ) -> set | list:
        set_len, list_len = len(in_set), len(in_list)
        return in_set if set_len < list_len else in_list

    @staticmethod
    def _get_tree_items(path: Path) -> list[tuple[str, str]]:
        return [item.stem.split("_") for item in path.iterdir() if item.is_file()]


if __name__ == "__main__":
    pg = PathGroup(paths=sqlpaths_factory)
    print(pg, len(pg.paths))
