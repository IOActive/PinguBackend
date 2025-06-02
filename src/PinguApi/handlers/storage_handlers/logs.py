import os
from PinguApi.handlers import storage
from PinguApi.storage_providers import utils
import logging

logger = logging.getLogger(__name__)

LOGS_FILES_SYNC_TIMEOUT = 60 * 60

class LogsStorage(object):
    """Storage logs handler."""

    def __init__(
        self,
        bucket_name,
        bucket_path="",
        log_results=True,
    ):
        """Inits the Logs.

        Args:
          bucket_name: Name of the bucket for logs synchronization.
          bucket_path: Path in the bucket where the logs are stored.
        """
        self._bucket_name = bucket_name
        self._bucket_path = bucket_path
        self._log_results = log_results
        self.storage_path = storage._provider().get_storage_path(bucket_name, bucket_path)
        self.cache_path = storage.cache.get_cache_folder_path(self.storage_path)

    @property
    def bucket_name(self):
        return self._bucket_name

    @property
    def bucket_path(self):
        return self._bucket_path
    
    def rsync_from_disk(
        self, timeout=LOGS_FILES_SYNC_TIMEOUT, delete=True
    ):
        """Upload cache files to Storage and remove files which do not exist locally.

        Args:
          timeout: Timeout for storage provider.
          delete: Whether or not to delete files on remote that don't exist locally.

        Returns:
          A bool indicating whether or not the command succeeded.
        """
        utils.legalize_storage_files(self.cache_path)
        return storage.sync_folder_to(self.storage_path)

    def rsync_to_disk(self, timeout=LOGS_FILES_SYNC_TIMEOUT, delete=True):
        """Download logs files from storage to cache path.

        Args:
          timeout: Timeout for storage provider.
          delete: Whether or not to delete files on disk that don't exist locally.

        Returns:
          A bool indicating whether or not the command succeeded.
        """

        return storage.sync_folder_from(self.storage_path)
        
    def write_log(self, data):
        """Writes a log from the cache to the bucket."""
        storage.write_data(data, self.storage_path)
