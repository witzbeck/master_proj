from dataclasses import dataclass
from functools import cached_property
from itertools import chain
from pathlib import Path

from pandas import DataFrame

from alexlib.files import Directory, File

from constants import DATA_PATH, QUERY_PATH, RAW_PATH

SOURCE_TABLES = {
    "LANDING_ASSESSMENTS",
    "LANDING_COURSES",
    "LANDING_STUDENT_ASSESSMENT",
    "LANDING_STUDENT_INFO",
    "LANDING_STUDENT_REGISTRATION",
    "LANDING_STUDENT_VLE",
    "LANDING_VLE",
}


@dataclass(frozen=True)
class StagingPathGroup:
    source_path: Path
    query_path: Path
    staging_path: Path


@dataclass
class QueriesDirectory(Directory):
    path: Path = QUERY_PATH

    @cached_property
    def schema_dict(self) -> dict[str, Directory]:
        """Return a dictionary of schema directories."""
        return {x.path.stem[x.path.stem.index("_") + 1 :]: x for x in self.dirlist}

    @property
    def landing_dir(self) -> Directory:
        """Return the landing directory."""
        return self.schema_dict["landing"]

    @cached_property
    def landing_query_dict(self) -> dict[str]:
        """Return a dictionary of landing queries."""
        return {x.path.stem: x for x in self.landing_dir.filelist}

    @property
    def allsqlfiles(self) -> list[File]:
        """Return a list of all SQL files."""
        return [x for x in self.allchildfiles if x.path.suffix == ".sql"]

    def get_sorted_schema_query_paths(self, schema: str) -> list[Path]:
        return sorted(
            [
                x.path
                for x in self.schema_dict[schema].filelist
                if x.path.suffix == ".sql"
            ],
            key=lambda x: str(x.parent),
        )

    def get_sorted_nonlanding_query_paths(self) -> list[Path]:
        return sorted(
            [x.path for x in self.allsqlfiles if "00_landing" not in x.path.parts],
            key=lambda x: str(x.parent),
        )

    @cached_property
    def path_lines_map(self) -> dict[Path, list[str]]:
        return {
            x.path: [line.strip().upper() for line in x.lines] for x in self.allsqlfiles
        }

    @cached_property
    def path_normalized_name_map(self) -> dict[str, set[str]]:
        return {file.path: file.path.stem.upper() for file in self.allsqlfiles}

    @cached_property
    def path_parent_order_map(self) -> dict[Path, int]:
        return {
            f.path: i
            for i, f in enumerate(
                sorted(self.allsqlfiles, key=lambda x: str(x.path.parent))
            )
        }

    @cached_property
    def path_source_map(self) -> dict[Path, set[str]]:
        # Get all lines with FROM or JOIN
        line_map = {
            path: [x for x in lines if "FROM " in x or "JOIN " in x]
            for path, lines in self.path_lines_map.items()
        }
        # Pair the index of FROM or JOIN with the line
        idx_map = {
            path: [
                (x.index("FROM "), x) if "FROM " in x else (x.index("JOIN "), x)
                for x in lines
            ]
            for path, lines in line_map.items()
        }
        # Slice the line to get the source
        return {
            path: {
                line[idx + 5 :].split()[0].strip(" ),;").replace(".", "_")
                for idx, line in idx_lines
                if len(line[idx + 5 :].split()[0]) > 3
                and "." in line[idx + 5 :].split()[0]
            }
            for path, idx_lines in idx_map.items()
        }

    @cached_property
    def target_source_df(self) -> DataFrame:
        df = DataFrame(
            chain.from_iterable(
                [
                    [
                        self.path_normalized_name_map[path],
                        source,
                        self.path_parent_order_map[path],
                    ]
                    for source in sources
                ]
                for path, sources in self.path_source_map.items()
            ),
            columns=["Target", "Source", "ParentOrder"],
        )
        df.loc[:, "ScaledParentOrder"] = (
            df.loc[:, "ParentOrder"] / df.loc[:, "ParentOrder"].max()
        )
        return df

    @cached_property
    def source_groupby(self) -> DataFrame:
        return (
            self.target_source_df.loc[:, ["Source", "Target"]]
            .groupby("Source")
            .count()
            .sort_values("Target", ascending=False)
        )

    @cached_property
    def source_ntargets_map(self) -> dict[str, int]:
        return self.source_groupby.to_dict()["Target"]

    @cached_property
    def target_groupby(self) -> DataFrame:
        return (
            self.target_source_df.loc[:, ["Source", "Target"]]
            .groupby("Target")
            .count()
            .sort_values("Source", ascending=False)
        )

    @cached_property
    def target_nsources_map(self) -> dict[str, int]:
        return self.target_groupby.to_dict()["Source"]

    @cached_property
    def sources_without_targets(self) -> set[str]:
        return (
            set(self.target_nsources_map.keys())
            - set(self.source_ntargets_map.keys())
            - SOURCE_TABLES
        )

    @cached_property
    def targets_without_sources(self) -> set[str]:
        return (
            set(self.source_ntargets_map.keys())
            - set(self.target_nsources_map.keys())
            - SOURCE_TABLES
        )


@dataclass
class DataDirectory(Directory):
    path: Path = DATA_PATH

    def make_subdir(self, name: str) -> Path:
        """Make a subdirectory."""
        (path := self.path / name).mkdir(exist_ok=True)
        return path

    @cached_property
    def export_path(self) -> Path:
        """Return the staging path."""
        return self.make_subdir("export")

    @cached_property
    def staging_path(self) -> Path:
        """Return the staging path."""
        return self.make_subdir("staging")

    @cached_property
    def source_path_dict(self) -> dict[str, Path]:
        """Return a dictionary of source paths."""
        return {x.stem: x for x in RAW_PATH.glob("*.csv")}

    @cached_property
    def staging_path_dict(self) -> dict[str, Path]:
        """Return a dictionary of staging paths."""
        return {
            x.stem: (self.staging_path / f"landing_{x.stem}").with_suffix(".parquet")
            for x in self.source_path_dict.values()
        }


def get_staging_path_groups(
    data_dir: DataDirectory, queries: QueriesDirectory
) -> list[StagingPathGroup]:
    """Return a list of StagingPathGroup objects."""
    return [
        StagingPathGroup(
            source_path=data_dir.source_path_dict[name],
            query_path=queries.landing_query_dict[name],
            staging_path=staging_path,
        )
        for name, staging_path in data_dir.staging_path_dict.items()
    ]
