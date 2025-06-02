from collections import namedtuple
from os import stat_result
import unittest
from unittest import mock
from PinguApi.storage_providers.storage_cache import StorageCache


class TestStorageCache(unittest.TestCase):

    def setUp(self):
        self.storage_cache = StorageCache("/mocked/cache/path")


    @mock.patch("os.path.exists", return_value=True)
    @mock.patch("os.utime")
    def test_update_access_timestamp(self, mock_utime, mock_exists):
        """Test updating the file access timestamp with mocks."""
        file_path = "/mocked/cache/file.txt"

        self.storage_cache.update_access_and_modification_timestamp(file_path)

        mock_utime.assert_called_once_with(file_path, None)


    @mock.patch("os.path.getsize", return_value=1234)
    @mock.patch("os.path.exists", return_value=True)
    @mock.patch(
        "PinguApi.storage_providers.utils.read_data_from_file", return_value={"size": 1234}
    )
    def test_file_exists_in_cache(self, mock_read_metadata, mock_exists, read_data_from_file):
        """Test checking if a file exists in cache with mocks."""
        file_path = "/mocked/cache/file.txt"

        result = self.storage_cache.file_exists_in_cache(file_path)

        assert result is True
        mock_read_metadata.assert_called_once()

    @mock.patch("os.utime", return_value=None)
    @mock.patch(
        "PinguApi.storage_providers.utils.read_data_from_file", return_value={"size": 1024}
    )    
    @mock.patch("os.path.exists", return_value=True)
    @mock.patch("os.path.getsize", return_value=1024)
    @mock.patch("PinguApi.utilities.shell.copy_file", return_value=True)
    def test_get_file_from_cache(self, mock_copy, mock_getsize, mock_exists, read_data_from_file, utime):
        """Test retrieving a file from cache with mocks."""
        file_path = "/mocked/local/file.txt"

        result = self.storage_cache.get_file_from_cache_if_exists(file_path)

        assert result is True
        mock_copy.assert_called_once()
        
    @mock.patch("os.listdir", return_value=["file1.txt", "file2.txt"])
    @mock.patch("os.stat")
    @mock.patch("os.path.getsize", return_value=1024)
    @mock.patch("os.utime", return_value=None)
    @mock.patch("os.path.exists", return_value=True)
    @mock.patch("os.makedirs", return_value=True)
    @mock.patch("PinguApi.utilities.shell.copy_file", return_value=True)
    @mock.patch("PinguApi.storage_providers.utils.write_data_to_file")
    def test_store_file_in_cache(self,
        mock_write_metadata, mock_copy, mock_makedirs, mock_exists, utime, getsize, stat, listdir
    ):
        """Test storing a file in cache with mocks."""
        file_path = "/mocked/source/file.txt"

        # Mocking os.stat to return a specific stat result
        stat_result = namedtuple('stat_result', ['st_mtime'])
        stat.return_value = stat_result(st_mtime=123456789)

        self.storage_cache.store_file_in_cache(file_path)

        mock_copy.assert_called_once()
        mock_write_metadata.assert_called_once()


    @mock.patch("PinguApi.utilities.shell.remove_file")
    def test_remove_cache_file(self, mock_remove):
        """Test removing a file from cache with mocks."""
        file_path = "/mocked/cache/file.txt"

        self.storage_cache.remove_cache_file_and_metadata(file_path)

        mock_remove.assert_any_call(self.storage_cache.get_cache_file_metadata_path(file_path))
        mock_remove.assert_any_call(file_path)

    @mock.patch("os.stat")
    @mock.patch("os.path.getsize", return_value=1024)
    @mock.patch("os.utime", return_value=None)
    @mock.patch("os.path.exists", return_value=True)
    @mock.patch("os.makedirs", return_value=True)
    @mock.patch("PinguApi.utilities.shell.copy_file", return_value=True)
    @mock.patch("PinguApi.storage_providers.utils.write_data_to_file")
    @mock.patch("os.listdir", return_value=[f"file_{i}.txt" for i in range(20)])
    @mock.patch("PinguApi.utilities.shell.remove_file")
    def test_cache_eviction(self, mock_remove, mock_listdir, write_data_to_file, copy_file, makedirs, 
                            exists, utime, getsize, stat
        ):
        """Test cache eviction logic with mocks."""
        # Mocking os.stat to return a specific stat result
        stat_result = namedtuple('stat_result', ['st_mtime'])
        stat.return_value = stat_result(st_mtime=123456789)
        self.storage_cache.store_file_in_cache("/mocked/source/file.txt")

        assert (
            mock_remove.call_count >= 5
        )  # Since MAX_CACHED_FILES_PER_DIRECTORY = 15, eviction should happen
