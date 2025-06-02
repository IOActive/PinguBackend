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
class BlobsStorage(object):
    """Blobs Storage handler."""

    def __init__(
        self,
        bucket_name,
        bucket_path="",
        log_results=True,
    ):
        """Inits the blobs storage handler.

        Args:
          bucket_name: Name of the bucket for corpus synchronization.
          bucket_path: Path in the bucket where the corpus is stored.
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
    
    def read_blob_to_disk(self, blob_key):
        """Reads a blob from the bucket and writes it to cache."""
        storage.copy_file_from(f"{self.storage_path}{blob_key}")
        
    def write_blob(self, data, blob_key, metadata=""):
        """Writes a blob from the cache to the bucket."""
        storage.write_data(data, f"{self.storage_path}{blob_key}", metadata)
        
    def remove_blob(self, blob_key):
        """Removes a blob from the bucket."""
        storage.delete(f"{self.storage_path}{blob_key}")

        
