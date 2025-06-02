# Copyright 2024 IOActive
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os
from PinguApi.handlers import storage
from PinguApi.storage_providers import utils
import logging

logger = logging.getLogger(__name__)

CORPUS_FILES_SYNC_TIMEOUT = 60 * 60
class CorpusStorage(object):
    """Minio Storage corpus."""

    def __init__(
        self,
        bucket_name,
        bucket_path="",
        log_results=True,
    ):
        """Inits the Corpus.

        Args:
          bucket_name: Name of the bucket for corpus synchronization.
          bucket_path: Path in the bucket where the corpus is stored.
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
        self, timeout=CORPUS_FILES_SYNC_TIMEOUT, delete=True
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

    def rsync_to_disk(self, timeout=CORPUS_FILES_SYNC_TIMEOUT, delete=True):
        """Download corpus files from storage to cache path.

        Args:
          timeout: Timeout for storage provider.
          delete: Whether or not to delete files on disk that don't exist locally.

        Returns:
          A bool indicating whether or not the command succeeded.
        """

        return storage.sync_folder_from(self.storage_path)

    def upload_corpus(self, data, file_name):
        """Upload the build to the storage."""
        return storage.write_data(data, f"{self.storage_path}/{file_name}")
      
    def download_corpus_to_cache(self, file_path):
        """Download the build to the cache."""
        return storage.copy_file_from(f"{self.storage_path}/{file_path}")
