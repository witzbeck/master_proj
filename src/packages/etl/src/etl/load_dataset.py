from functools import partial
from hashlib import md5
from logging import getLogger
from pathlib import Path
from zipfile import ZipFile

from requests import get

from core import RAW_PATH
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


def download_file(url: str, path: Path) -> None:
    """Download a file."""
    logger.info(f"Downloading dataset from {url} to {path}.")
    with get(url, stream=True) as response:
        response.raise_for_status()
        with path.open("wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
    logger.info(f"Downloaded dataset to {path}.")


download_dataset = partial(download_file, OULAD_URL, DATASET_PATH)
download_checksum = partial(download_file, OULAD_MD5_URL, CHECKSUM_PATH)


def validate_checksum(file_path: Path, checksum_path: Path = CHECKSUM_PATH) -> bool:
    """Validate the checksum of a file."""
    logger.info(f"Validating checksum of {file_path}.")
    with file_path.open("rb") as file:
        checksum = md5(file.read()).hexdigest()
    expected = checksum_path.read_bytes().decode().strip()
    if checksum != expected:
        logger.error(f"Checksum mismatch: {checksum} != {expected}.")
        return False
    logger.info(f"Checksum validated: {checksum} == {expected}.")
    return True


def unzip_file(zip_path: Path, extract_path: Path = EXTRACT_PATH) -> None:
    """Unzip a file."""
    logger.info(f"Unzipping {zip_path} to {extract_path}.")
    with ZipFile(zip_path, "r") as file:
        file.extractall(extract_path)
    logger.info(f"Unzipped {zip_path} to {extract_path}.")


def load_dataset() -> None:
    """Download and extract the dataset."""
    if not DATASET_PATH.exists():
        download_dataset()
    if not CHECKSUM_PATH.exists():
        download_checksum()
    if validate_checksum(DATASET_PATH):
        unzip_file(DATASET_PATH)
    else:
        logger.error("Failed to validate checksum.")
    for orig, dest in SOURCE_TABLE_MAP.items():
        (EXTRACT_PATH / f"{orig}.csv").rename(RAW_PATH / f"{dest}.csv")


if __name__ == "__main__":
    load_dataset()
