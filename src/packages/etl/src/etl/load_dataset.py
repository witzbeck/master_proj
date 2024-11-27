from functools import partial
from hashlib import md5
from logging import getLogger
from pathlib import Path
from zipfile import ZipFile

from requests import get
from tqdm import tqdm

from packages.core import RAW_PATH

from etl.constants import OULAD_MD5_URL, OULAD_URL

logger = getLogger(__name__)
SOURCE_TABLE_MAP = {
    "assessments": "assessments",
    "courses": "courses",
    "studentAssessment": "student_assessment",
    "studentInfo": "student_info",
    "studentRegistration": "student_registration",
    "studentVle": "student_vle",
    "vle": "vle",
}
DATASET_PATH = RAW_PATH / "dataset.zip"
CHECKSUM_PATH = RAW_PATH / "dataset.md5"
EXTRACT_PATH = RAW_PATH
EXTRACT_CSV_PATHS = [EXTRACT_PATH / f"{table}.csv" for table in SOURCE_TABLE_MAP.keys()]
RAW_CSV_PATHS = [RAW_PATH / f"{table}.csv" for table in SOURCE_TABLE_MAP.values()]


def download_file(url: str, path: Path, force: bool = False) -> None:
    """Download a file."""
    if force and path.exists():
        path.unlink()
        logger.info(f"Deleted existing file at {path}.")
    if path.exists():
        logger.info(f"File already exists at {path}.")
        return
    logger.info(f"Downloading dataset from {url} to {path}.")
    with get(url, stream=True) as response:
        response.raise_for_status()
        with path.open("wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
    logger.info(f"Downloaded {path.name} to {path.parent}.")


def download_dataset(force: bool = False) -> None:
    """Download the dataset."""
    download_file(OULAD_URL, DATASET_PATH, force=force)
    logger.info("Downloaded dataset.")


def download_checksum(force: bool = False) -> None:
    """Download the checksum."""
    download_file(OULAD_MD5_URL, CHECKSUM_PATH, force=force)
    logger.info("Downloaded checksum.")


def validate_checksum(file_path: Path, checksum_path: Path = CHECKSUM_PATH) -> bool:
    """Validate the checksum of a file."""
    logger.info(f"Validating checksum of {file_path}.")
    with file_path.open("rb") as file:
        checksum = md5(file.read()).hexdigest()
    expected = checksum_path.read_bytes().decode().strip()
    if checksum != expected:
        logger.critical(f"Checksum mismatch: {checksum} != {expected}.")
        return False
    logger.info(f"Checksum validated: {checksum} == {expected}.")
    return True


def unzip_file(zip_path: Path, extract_path: Path = EXTRACT_PATH) -> None:
    """Unzip a file."""
    logger.info(f"Unzipping {zip_path} to {extract_path}.")
    with ZipFile(zip_path, "r") as file:
        file.extractall(extract_path)
    logger.info(f"Unzipped {zip_path} to {extract_path}.")


def check_files_exist(file_paths: list[Path]) -> bool:
    """Check if the files exist."""
    return all(file_path.exists() for file_path in file_paths)


extract_files_exist = partial(check_files_exist, EXTRACT_CSV_PATHS)
raw_files_exist = partial(check_files_exist, RAW_CSV_PATHS)


def unzip_dataset(force: bool = False, cleanup: bool = True) -> None:
    """Unzip the dataset."""
    files_exist = extract_files_exist()
    if files_exist and force:
        for file_path in tqdm(EXTRACT_CSV_PATHS, desc="Cleaning up (extracted)"):
            file_path.unlink(missing_ok=True)
    if files_exist:
        logger.info("Files already extracted.")
    elif validate_checksum(DATASET_PATH):
        unzip_file(DATASET_PATH)
    else:
        logger.critical("Failed to validate checksum.")
    if cleanup:
        DATASET_PATH.unlink(missing_ok=True)
        logger.info("Deleted dataset.zip.")


def rename_files(force: bool = False, cleanup: bool = True) -> None:
    """Rename the files."""
    files_exist = raw_files_exist()
    if files_exist and force:
        for file_path in tqdm(RAW_CSV_PATHS, desc="Cleaning up (raw)"):
            file_path.unlink(missing_ok=True)
    if files_exist:
        logger.info("Files already renamed.")
    else:
        for orig, dest in tqdm(
            zip(EXTRACT_CSV_PATHS, RAW_CSV_PATHS, strict=True), desc="Renaming files"
        ):
            orig.rename(dest)
    if cleanup:
        for file_path in tqdm(EXTRACT_CSV_PATHS, desc="Cleaning up"):
            file_path.unlink(missing_ok=True)


def load_dataset(force: bool = False, cleanup: bool = True) -> None:
    """Download and extract the dataset."""
    if raw_files_exist() and not force:
        logger.info("Dataset already loaded.")
        return
    download_dataset(force=force)
    download_checksum(force=force)
    unzip_dataset(force=force, cleanup=cleanup)
    if cleanup:
        DATASET_PATH.unlink(missing_ok=True)
        CHECKSUM_PATH.unlink(missing_ok=True)
        logger.info("Deleted dataset.zip and dataset.md5.")
    rename_files(force=force, cleanup=cleanup)


if __name__ == "__main__":
    load_dataset()
