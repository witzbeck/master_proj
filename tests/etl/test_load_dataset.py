from hashlib import md5
from pathlib import Path
from unittest.mock import MagicMock, call, patch

from pytest import mark

from etl.load_dataset import download_file, load_dataset, unzip_file, validate_checksum


@mark.parametrize(
    "force, file_exists",
    [
        (False, False),  # File doesn't exist, force=False
        (False, True),  # File exists, force=False
        (True, True),  # File exists, force=True
    ],
)
def test_download_file(force, file_exists):
    with (
        patch("etl.load_dataset.get") as mock_get,
        patch("etl.load_dataset.logger") as mock_logger,
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
        mock_path.name = "dataset.zip"
        mock_path.parent = Path("/path/to")

        # Setup exists() behavior
        if file_exists:
            if force:
                # File exists at first, but after unlink it doesn't
                mock_path.exists.side_effect = [True, False]
            else:
                # File exists, and remains existing
                mock_path.exists.return_value = True
        else:
            mock_path.exists.return_value = False

        # Call the function
        download_file("http://example.com/dataset.zip", mock_path, force=force)

        if file_exists and not force:
            # Should log that file already exists and not download
            mock_logger.info.assert_any_call(f"File already exists at {mock_path}.")
            mock_get.assert_not_called()
            mock_path.unlink.assert_not_called()
        else:
            if file_exists and force:
                # Should delete existing file
                mock_path.unlink.assert_called_once()
                mock_logger.info.assert_any_call(
                    f"Deleted existing file at {mock_path}."
                )
            else:
                mock_path.unlink.assert_not_called()
            # Should proceed with download
            mock_get.assert_called_once_with(
                "http://example.com/dataset.zip", stream=True
            )
            mock_response.raise_for_status.assert_called_once()
            mock_response.iter_content.assert_called_once_with(chunk_size=8192)
            mock_path.open.assert_called_once_with("wb")
            mock_file.write.assert_has_calls([call(b"chunk1"), call(b"chunk2")])
            mock_logger.info.assert_any_call(
                f"Downloading dataset from http://example.com/dataset.zip to {mock_path}."
            )
            mock_logger.info.assert_any_call(
                f"Downloaded {mock_path.name} to {mock_path.parent}."
            )


@mark.parametrize("checksum_match", [True, False])
def test_validate_checksum(checksum_match):
    with (
        patch("etl.load_dataset.logger") as mock_logger,
    ):
        # Prepare mock paths
        mock_file_path = MagicMock(spec=Path)
        mock_checksum_path = MagicMock(spec=Path)
        mock_file_path.name = "dataset.zip"

        # The content of the file
        file_content = b"test data"
        # The expected checksum
        expected_md5 = md5(file_content).hexdigest()

        # Mock file_path.open()
        mock_file_handle = MagicMock()
        mock_file_handle.read.return_value = file_content
        mock_file_context = MagicMock()
        mock_file_context.__enter__.return_value = mock_file_handle
        mock_file_path.open.return_value = mock_file_context

        # Mock checksum_path.read_bytes()
        if checksum_match:
            mock_checksum_path.read_bytes.return_value = f"{expected_md5}\n".encode()
        else:
            mock_checksum_path.read_bytes.return_value = b"wrongchecksum\n"

        # Call the function
        result = validate_checksum(mock_file_path, checksum_path=mock_checksum_path)

        if checksum_match:
            assert result
            mock_logger.info.assert_any_call(
                f"Checksum validated: {expected_md5} == {expected_md5}."
            )
        else:
            assert not result
            mock_logger.critical.assert_any_call(
                f"Checksum mismatch: {expected_md5} != wrongchecksum."
            )


def test_unzip_file():
    with (
        patch("etl.load_dataset.ZipFile") as mock_zipfile_class,
        patch("etl.load_dataset.logger") as mock_logger,
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


@mark.parametrize(
    "raw_files_exist_return_value, force, cleanup",
    [
        (True, False, True),  # Files exist, force=False
        (False, False, True),  # Files don't exist, force=False
        (False, True, False),  # Files don't exist, force=True, no cleanup
    ],
)
def test_load_dataset(tmp_path, raw_files_exist_return_value, force, cleanup):
    # Setup temporary paths
    dataset_path = tmp_path / "dataset.zip"
    checksum_path = tmp_path / "dataset.md5"
    extract_path = tmp_path
    raw_path = tmp_path

    with (
        patch("etl.load_dataset.DATASET_PATH", dataset_path),
        patch("etl.load_dataset.CHECKSUM_PATH", checksum_path),
        patch("etl.load_dataset.EXTRACT_PATH", extract_path),
        patch("etl.load_dataset.RAW_PATH", raw_path),
        patch("etl.load_dataset.download_dataset") as mock_download_dataset,
        patch("etl.load_dataset.download_checksum") as mock_download_checksum,
        patch("etl.load_dataset.validate_checksum", return_value=True),
        patch("etl.load_dataset.unzip_dataset") as mock_unzip_dataset,
        patch("etl.load_dataset.rename_files") as mock_rename_files,
        patch("etl.load_dataset.logger") as mock_logger,
        patch(
            "etl.load_dataset.raw_files_exist",
            return_value=raw_files_exist_return_value,
        ),
        patch("pathlib.Path.unlink") as mock_unlink,
    ):
        # Call the load_dataset function
        load_dataset(force=force, cleanup=cleanup)

        if raw_files_exist_return_value and not force:
            # Should log that dataset is already loaded and return
            mock_logger.info.assert_called_once_with("Dataset already loaded.")
            mock_download_dataset.assert_not_called()
            mock_download_checksum.assert_not_called()
            mock_unzip_dataset.assert_not_called()
            mock_rename_files.assert_not_called()
        else:
            # Should proceed with downloading and processing
            mock_download_dataset.assert_called_once_with(force=force)
            mock_download_checksum.assert_called_once_with(force=force)
            mock_unzip_dataset.assert_called_once_with(force=force, cleanup=cleanup)
            mock_rename_files.assert_called_once_with(force=force, cleanup=cleanup)
            if cleanup:
                # Should unlink dataset and checksum files
                assert mock_unlink.call_count == 2  # dataset.zip and dataset.md5
                mock_logger.info.assert_any_call("Deleted dataset.zip and dataset.md5.")
            else:
                mock_unlink.assert_not_called()
