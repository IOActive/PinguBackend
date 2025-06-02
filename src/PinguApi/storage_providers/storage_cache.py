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

import datetime
import os
from PinguApi.storage_providers import utils
from PinguApi.utilities import shell
import logging
import time

# File extension for tmp cache files.
CACHE_METADATA_FILE_EXTENSION = ".metadata"
# Maximum size of file to allow in cache.
CACHE_SIZE_LIMIT = 5 * 1024 * 1024 * 1024  # 5 GB
# Maximum number of cached files per directory.
MAX_CACHED_FILES_PER_DIRECTORY = 15
# Wait time to let NFS copy to sync across bricks.
CACHE_COPY_WAIT_TIME = 1

logger = logging.getLogger(__name__)


class StorageCache:
    def __init__(self, path) -> None:
        self.cache_path = path

    def update_access_and_modification_timestamp(self, file_path):
        os.utime(file_path, None)

    def get_cache_file_size_from_metadata(self, cache_file_path):
        """Return cache file size from metadata file."""
        cache_file_metadata_path = self.get_cache_file_metadata_path(cache_file_path)
        metadata_content = utils.read_data_from_file(
            cache_file_metadata_path, eval_data=True
        )

        if not metadata_content or "size" not in metadata_content:
            return None

        return metadata_content["size"]

    def get_cache_file_metadata_path(self, cache_file_path):
        """Return metadata file path for a cache file."""
        return "%s%s" % (cache_file_path, CACHE_METADATA_FILE_EXTENSION)

    def file_exists_in_cache(self, cache_file_path):
        """Returns if the file exists in cache."""
        cache_file_metadata_path = self.get_cache_file_metadata_path(cache_file_path)
        if not os.path.exists(cache_file_metadata_path):
            return False

        if not os.path.exists(cache_file_path):
            return False

        actual_cache_file_size = os.path.getsize(cache_file_path)
        expected_cache_file_size = self.get_cache_file_size_from_metadata(
            cache_file_path
        )
        return actual_cache_file_size == expected_cache_file_size

    def get_cache_file_path(self, file_path):
        """Return cache file path given a local file path."""
        return os.path.join(
            self.cache_path,
            utils.get_directory_hash_for_path(file_path),
            os.path.basename(file_path),
        )
    
    def get_cache_folder_path(self, file_path):
        """Return cache folder path given a local file path."""
        return os.path.join(
            self.cache_path,
            utils.get_directory_hash_for_path(file_path),
        )

    def get_file_from_cache_if_exists(
        self, file_path, update_modification_time_on_access=True
    ):
        """Get file from cache if available."""
        cache_file_path = self.get_cache_file_path(file_path)
        if not cache_file_path or not self.file_exists_in_cache(cache_file_path):
            # If the file does not exist in cache, bail out.
            return False

        # Fetch cache file size before starting the actual copy.
        cache_file_size = self.get_cache_file_size_from_metadata(cache_file_path)

        # Copy file from cache to local.
        if not shell.copy_file(cache_file_path, file_path):
            return False

        # Update timestamp to later help with eviction of old files.
        if update_modification_time_on_access:
            self.update_access_and_modification_timestamp(cache_file_path)

        # Return success or failure based on existence of local file and size
        # comparison.
        return (
            os.path.exists(file_path) and os.path.getsize(file_path) == cache_file_size
        )

    def write_cache_file_metadata(self, cache_file_path, file_path):
        """Write cache file metadata."""
        cache_file_metadata_path = self.get_cache_file_metadata_path(cache_file_path)
        utils.write_data_to_file(
            {"size": os.path.getsize(file_path)}, cache_file_metadata_path
        )

    def remove_cache_file_and_metadata(self, cache_file_path):
        """Removes cache file and its metadata."""
        shell.remove_file(self.get_cache_file_metadata_path(cache_file_path))
        shell.remove_file(cache_file_path)

    def store_file_in_cache(
        self, file_path, cached_files_per_directory_limit=True, force_update=False
    ):
        """Get file from pingu_sdk.nfs cache if available."""
        if not os.path.exists(file_path):
            logger.error(
                "Local file %s does not exist, nothing to store in cache." % file_path
            )
            return

        if os.path.getsize(file_path) > CACHE_SIZE_LIMIT:
            logger.info("File %s is too large to store in cache, skipping." % file_path)
            return

        # If cache  is not available due to heavy load, skip storage operation
        # altogether as we would fail to store file.
        if not os.path.exists(
            os.path.join(self.cache_path, ".")
        ):  # Use . to iterate mount.
            logger.warning("Cache %s not available." % self.cache_path)
            return

        cache_file_path = self.get_cache_file_path(file_path)
        cache_directory = os.path.dirname(cache_file_path)
        filename = os.path.basename(file_path)

        if not os.path.exists(cache_directory):
            if not shell.create_directory(cache_directory, create_intermediates=True):
                logger.error("Failed to create cache directory %s." % cache_directory)
                return

        # Check if the file already exists in cache.
        if self.file_exists_in_cache(cache_file_path):
            if not force_update:
                return

            # If we are forcing update, we need to remove current cached file and its
            # metadata.
            self.remove_cache_file_and_metadata(cache_file_path)

        # Delete old cached files beyond our maximum storage limit.
        if cached_files_per_directory_limit:
            # Get a list of cached files.
            cached_files_list = []
            for cached_filename in os.listdir(cache_directory):
                if cached_filename.endswith(CACHE_METADATA_FILE_EXTENSION):
                    continue
                cached_file_path = os.path.join(cache_directory, cached_filename)
                cached_files_list.append(cached_file_path)

            mtime = lambda f: os.stat(f).st_mtime
            last_used_cached_files_list = list(
                sorted(cached_files_list, key=mtime, reverse=True)
            )
            for cached_file_path in last_used_cached_files_list[
                MAX_CACHED_FILES_PER_DIRECTORY - 1 :
            ]:
                self.remove_cache_file_and_metadata(cached_file_path)

        # Start storing the actual file in cache now.
        logger.info("Started storing file %s into cache." % filename)

        # Check if another bot already updated it.
        if self.file_exists_in_cache(cache_file_path):
            return

        shell.copy_file(file_path, cache_file_path)
        self.write_cache_file_metadata(cache_file_path, file_path)
        time.sleep(CACHE_COPY_WAIT_TIME)
        error_occurred = not self.file_exists_in_cache(cache_file_path)

        if error_occurred:
            logger.error("Failed to store file %s into cache." % filename)
        else:
            logger.info("Completed storing file %s into cache." % filename)

    def get_cache_last_updated(self, cache_path):
        """Get the last modification time of a cached file, if it exists."""
        last_update = None
        for dir_path, _, files in os.walk(cache_path):
            for blob in files:
                file_path = os.path.join(dir_path, blob)
                mtime = os.path.getmtime(file_path)
                if not last_update or mtime > last_update:
                    last_update = mtime
                    
        if type(last_update) is float:
            # Remove UTC tzinfo to make these comparable.
            last_update = datetime.datetime.fromtimestamp(last_update).replace(tzinfo=None)
        elif type(last_update) is datetime.datetime:
            last_update = last_update.replace(tzinfo=None)
        return last_update


    def get_file_size_from_cache_if_exists(self, file_path):
        """Get file size from pingu_sdk.nfs cache if available."""
        cache_file_path = self.get_cache_file_path(file_path)
        if not cache_file_path or not self.file_exists_in_cache(cache_file_path):
            # If the file does not exist in cache, bail out.
            return None

        return self.get_cache_file_size_from_metadata(cache_file_path)