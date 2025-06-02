import os
from PinguApi.handlers import storage
from PinguApi.storage_providers import utils
import logging

logger = logging.getLogger(__name__)

class BuildStorage(object):
    """Storage build handler"""

    def __init__(
        self,
        bucket_name,
        bucket_path="",
        log_results=True,
    ):
        """Inits the Build.

        Args:
          bucket_name: Name of the bucket for build synchronization.
          bucket_path: Path in the bucket where the build is stored.
        """
        self._bucket_name = bucket_name
        self._bucket_path = bucket_path
        self._log_results = log_results
        self.storage_path = storage._provider().get_storage_path(bucket_name, bucket_path)
        self.cache_path = storage.cache.get_cache_file_path(self.storage_path)

    @property
    def bucket_name(self):
        return self._bucket_name

    @property
    def bucket_path(self):
        return self._bucket_path

    def get_build_size(self, path):
        """Get the size of the build."""
        return storage.get_object_size(path)

    def download_build_to_cache(self, file_path):
        """Download the build to the cache."""
        return storage.copy_file_from(f"{self.storage_path}/{file_path}")

    def get_target_list(self, target_list='targets.list'):
        """Get the target list from the build."""
        storage_path = f"{self.storage_path}/{target_list}"
        if not storage.exists(storage_path):
            logger.error(f"Target list {target_list} not found in {target_list}.")
            return None
        return storage.read_data(storage_path)

    def upload_build_from_cache(self, data, file_name):
        """Upload the build to the storage."""
        return storage.write_data(data, f"{self.storage_path}/{file_name}")
    
    def delete_build(self, build_file):
        """Delete the build from the storage."""
        return storage.delete(f"{self.storage_path}/{build_file}")
    
    def list_builds(self):
        return storage.list_blobs(self.storage_path)
    
    def create_target_list(self):
        storage.write_data(b'', f"{self.storage_path}/targets.list")
        
    def write_targets_list(self, new_content):
        storage.write_data(new_content, f"{self.storage_path}/targets.list")
        