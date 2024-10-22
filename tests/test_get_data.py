from hashlib import md5
from pathlib import Path
from unittest.mock import MagicMock, call, mock_open, patch

from utils.get_dataset import download_file, main, unzip_file, validate_checksum


def test_download_file():
    with (
        patch("utils.get_dataset.get") as mock_get,
        patch("utils.get_dataset.logger") as mock_logger,
    ):
        # Mock the response from get
        mock_response = MagicMock()
        mock_response.iter_content.return_value = [b"chunk1", b"chunk2"]
        mock_response.raise_for_status = MagicMock()
        mock_response.__enter__.return_value = mock_response
        mock_get.return_value = mock_response

        # Mock the file path and file writing
        mock_path = MagicMock(spec=Path)
        mock_file = MagicMock()
        mock_path.open.return_value.__enter__.return_value = mock_file

        # Call the function
        download_file("http://example.com/dataset.zip", mock_path)

        # Assertions
        mock_get.assert_called_once_with("http://example.com/dataset.zip", stream=True)
        mock_response.raise_for_status.assert_called_once()
        mock_response.iter_content.assert_called_once_with(chunk_size=8192)
        mock_path.open.assert_called_once_with("wb")
        mock_file.write.assert_has_calls([call(b"chunk1"), call(b"chunk2")])
        mock_logger.info.assert_any_call(
            f"Downloading dataset from http://example.com/dataset.zip to {mock_path}."
        )
        mock_logger.info.assert_any_call(f"Downloaded dataset to {mock_path}.")


def test_validate_checksum():
    with (
        patch("utils.get_dataset.logger") as mock_logger,
        patch("pathlib.Path.open", mock_open(read_data=b"test data")),
        patch("pathlib.Path.read_bytes") as mock_read_bytes,
    ):
        # Prepare mock paths
        mock_file_path = Path("/path/to/dataset.zip")
        mock_checksum_path = Path("/path/to/dataset.md5")

        # Calculate expected MD5 checksum
        expected_md5 = md5(b"test data").hexdigest()

        # Mock read_bytes to return expected checksum
        mock_read_bytes.return_value = f"{expected_md5}\n".encode()

        # Call the function
        result = validate_checksum(mock_file_path, mock_checksum_path)

        # Assertions
        assert result
        mock_logger.info.assert_any_call(
            f"Checksum validated: {expected_md5} == {expected_md5}."
        )

        # Test checksum mismatch
        mock_read_bytes.return_value = b"wrongchecksum\n"
        result = validate_checksum(mock_file_path, mock_checksum_path)
        assert not result
        mock_logger.error.assert_called_with(
            f"Checksum mismatch: {expected_md5} != wrongchecksum."
        )


def test_unzip_file():
    with (
        patch("utils.get_dataset.ZipFile") as mock_zipfile_class,
        patch("utils.get_dataset.logger") as mock_logger,
    ):
        # Mock the ZipFile instance
        mock_zipfile = MagicMock()
        mock_zipfile_class.return_value.__enter__.return_value = mock_zipfile

        # Call the function
        zip_path = Path("/path/to/dataset.zip")
        extract_path = Path("/path/to/extract")
        unzip_file(zip_path, extract_path)

        # Assertions
        mock_zipfile_class.assert_called_once_with(zip_path, "r")
        mock_zipfile.extractall.assert_called_once_with(extract_path)
        mock_logger.info.assert_any_call(f"Unzipping {zip_path} to {extract_path}.")
        mock_logger.info.assert_any_call(f"Unzipped {zip_path} to {extract_path}.")


def test_main(tmp_path):
    # Setup temporary paths
    dataset_path = tmp_path / "dataset.zip"
    checksum_path = tmp_path / "dataset.md5"
    extract_path = tmp_path
    raw_path = tmp_path

    # Define a side effect function for Path.exists()
    def exists_side_effect(self):
        if self == dataset_path:
            # First call returns False (to trigger download), second call returns True
            return exists_side_effect.dataset_path_exists.pop(0)
        elif self == checksum_path:
            return exists_side_effect.checksum_path_exists.pop(0)
        else:
            # Return True for other paths
            return True

    # Initialize the side effect lists
    exists_side_effect.dataset_path_exists = [False, True]
    exists_side_effect.checksum_path_exists = [False, True]

    # Define a side effect for unzip_file to simulate file extraction
    def unzip_side_effect(zip_path, extract_path=extract_path):
        # Simulate extraction by creating the files that 'main()' expects
        for orig in ["assessments"]:
            file_path = extract_path / f"{orig}.csv"
            file_path.touch()

    # Mock constants and functions
    with (
        patch("utils.get_dataset.DATASET_PATH", dataset_path),
        patch("utils.get_dataset.CHECKSUM_PATH", checksum_path),
        patch("utils.get_dataset.EXTRACT_PATH", extract_path),
        patch("utils.get_dataset.RAW_PATH", raw_path),
        patch("utils.get_dataset.download_dataset") as mock_download_dataset,
        patch("utils.get_dataset.download_checksum") as mock_download_checksum,
        patch(
            "utils.get_dataset.validate_checksum", return_value=True
        ) as mock_validate_checksum,
        patch(
            "utils.get_dataset.unzip_file", side_effect=unzip_side_effect
        ) as mock_unzip_file,
        patch("utils.get_dataset.logger"),
        patch(
            "utils.get_dataset.SOURCE_TABLE_MAP", {"assessments": "assessments_renamed"}
        ),
        patch("pathlib.Path.exists", new=exists_side_effect),
    ):
        # Call the main function
        main()

        # Assertions
        mock_download_dataset.assert_called_once()
        mock_download_checksum.assert_called_once()
        mock_validate_checksum.assert_called_once_with(dataset_path)
        mock_unzip_file.assert_called_once_with(dataset_path)

        # Expected destination files
        dest_file = raw_path / "assessments_renamed.csv"

        # Assertions for file renaming
        assert dest_file.exists()
