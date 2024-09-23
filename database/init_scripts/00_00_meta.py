from collections.abc import Generator
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
    parent: Path = None
    pattern: str = None

    def __post_init__(self) -> None:
        if isinstance(self.paths, Generator):
            self.paths = list(self.paths)
        if self.paths
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
    
    @classmethod
    def from_parent(cls, parent: Path, pattern: str) -> "PathGroup":
        lst = parent.iterdir()
        return cls(parent=parent, pattern=pattern)


if __name__ == "__main__":
    pg = PathGroup(parent=(here.parent / "_init_scripts"),paths=sqlpaths_factory)
    print(pg, len(pg.paths))
    for path in pg.paths:
        if "_db_" in path.stem:
            new_stem = path.stem.replace("_db_", "_")
            new_path = path.with_stem(new_stem)
            path.rename(new_path)
        print(path)
