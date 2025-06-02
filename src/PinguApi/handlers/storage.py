"""Functions for managing Storage."""

import datetime
import logging
import os
import time
from django.conf import settings
from minio import S3Error
import yaml
from PinguApi.storage_providers.storage_provider import StorageProvider
from PinguApi.storage_providers.file_system_provider import FileSystemProvider
from PinguApi.storage_providers.minio_provider import MinioProvider
from PinguApi.utilities import configuration
from PinguApi.submodels.project import Project
from PinguApi.storage_providers.storage_cache import StorageCache

# Usually, authentication time have expiry of ~30 minutes, but keeping this
# values lower to avoid failures and any future changes.

CREATE_BUCKET_DELAY = 4

logger = logging.getLogger(__name__)

cache = None
if settings.CACHE_PATH:
    cache = StorageCache(path=settings.CACHE_PATH)


def _provider() -> StorageProvider:
    """Get the current storage provider."""
    local_buckets_path = settings.LOCAL_STORAGE_PATH
    if local_buckets_path != 'None':
        return FileSystemProvider(local_buckets_path)

    return MinioProvider(
        host=settings.MINIO_HOST,
        access_key=settings.MINIO_ACCESS_KEY,
        secret_key=settings.MINIO_SECRET_KEY,
    )


def create_bucket_if_needed(bucket_name, object_lifecycle=None, cors=None):
    """Creates a bucket."""
    provider = _provider()
    if provider.get_bucket(bucket_name):
        return True

    if not provider.create_bucket(bucket_name, object_lifecycle, cors):
        return False

    time.sleep(CREATE_BUCKET_DELAY)
    return True

def delete_bucket(bucket_name):
    """Deletes a bucket."""
    return _provider().delete_bucket(bucket_name)

def copy_file_from(storage_file_path):
    """Copies a file from storage to the cache."""
    if not cache:
        logger.error("Cache is not enabled, cannot retrieve files.")
        return False

    cache_path = cache.get_cache_file_path(storage_file_path)

    if cache.get_file_from_cache_if_exists(storage_file_path):
        logger.info(f"Copied file {storage_file_path} from cache.")
        return True

    if not _provider().copy_file_from(storage_file_path, cache_path):
        return False

    return True

def copy_file_to(
    local_file_path_or_handle, storage_file_path, metadata=None, size=None
):
    """Copy local file to a storage path."""
    if isinstance(local_file_path_or_handle, str) and not os.path.exists(
        local_file_path_or_handle
    ):
        logger.error("Local file %s not found." % local_file_path_or_handle)
        return False

    return _provider().copy_file_to(
        local_file_path_or_handle, storage_file_path, metadata=metadata, size=size
    )


def copy_blob(storage_source_path, storage_target_path):
    """Copy two blobs on storage without touching local disk."""
    return _provider().copy_blob(storage_source_path, storage_target_path)


def delete(storage_file_path):
    """Delete a storage file given its path."""
    cache.remove_cache_file_and_metadata(storage_file_path)
    return _provider().delete(storage_file_path)


def exists(storage_file_path, ignore_errors=False):
    """Return whether if a storage file exists."""
    try:
        return bool(_provider().get(storage_file_path))
    except S3Error:
        if not ignore_errors:
            logger.error(
                "Failed when trying to find storage file %s." % storage_file_path
            )
            if (cache.get_file_from_cache_if_exists(storage_file_path)):
                logger.warning("Found in cache, but failed to get from storege.")
                cache.remove_cache_file_and_metadata(storage_file_path)
                logger.warning("Removed from cache.")
        return False


def last_updated(storage_file_path):
    """Return last updated value by parsing stats for all blobs under a storage path."""
    last_update = None
    for blob in _provider().list_blobs(storage_file_path):
        if not last_update or blob["updated"] > last_update:
            last_update = blob["updated"]
    if last_update:
        # Remove UTC tzinfo to make these comparable.
        last_update = last_update.replace(tzinfo=None)
    return last_update


def read_data(storage_file_path):
    """Return content of a storage file."""
    return _provider().read_data(storage_file_path)


def write_data(data, storage_file_path, metadata=""):
    """Return content of a storage file."""
    return _provider().write_data(data, storage_file_path, metadata=metadata)


def get_blobs(storage_path, recursive=True):
    """Return blobs under the given storage path."""
    for blob in _provider().list_blobs(storage_path, recursive=recursive):
        yield blob


def list_blobs(storage_path, recursive=True):
    """Return blob names under the given storage path."""
    for blob in _provider().list_blobs(storage_path, recursive=recursive):
        yield blob


def get_download_file_size(storage_file_path):
    """Get file size from cache or storage."""
    if cache:
        size_from_cache = cache.get_file_size_from_cache_if_exists(storage_file_path)
        if size_from_cache is not None:
            return size_from_cache
    return get_object_size(storage_file_path)

def get(storage_file_path):
    """Get object data."""
    return _provider().get(storage_file_path)


def get_object_size(storage_file_path):
    """Get the metadata for a file."""
    return _provider().get(storage_file_path)["size"]


def blobs_bucket(project: Project):
    """Get the blobs bucket name."""
    return configuration.get_value(
        key_path="blobs.bucket", config=yaml.safe_load(project.configuration)
    )

def sync_folder_from(storage_path):
    """Syncs a remote folder from storage directly into the cache, ensuring it's up-to-date."""
    provider = _provider()
    cache_path = cache.get_cache_folder_path(storage_path)
    storage_last_updated = last_updated(storage_path)
    cache_last_updated = cache.get_cache_last_updated(cache_path)

    # If cache exists and is up-to-date, use it
    if cache_last_updated and storage_last_updated and cache_last_updated >= storage_last_updated:
        logger.info(f"Using cached folder {storage_path}.")
        return True  # No need to sync

    logger.info(f"Cache outdated for {storage_path}. Syncing from storage.")

    # Perform sync directly into the cache
    return provider.sync_folder_from(local_path=cache_path, remote_path=storage_path)

def sync_folder_to(storage_path, delete=False):
    """
    Syncs a folder from cache to storage, ensuring only updated files are uploaded.
    """
    provider = _provider()
    
    if not cache:
        logger.warning("Cache is not enabled. Cannot sync folder to storage.")
        return False

    cache_path = cache.get_cache_folder_path(storage_path)

    # Ensure the folder exists in cache
    if not os.path.exists(cache_path):
        logger.error(f"Cache folder does not exist: {cache_path}")
        return False

    storage_last_updated = last_updated(storage_path)
    cache_last_updated = cache.get_cache_last_updated(cache_path)

    # If storage is already up-to-date, no need to sync
    if cache_last_updated and storage_last_updated and cache_last_updated <= storage_last_updated:
        logger.info(f"Storage folder {storage_path} is already up-to-date. Skipping sync.")
        return True  

    logger.info(f"Syncing folder {storage_path} from cache to storage.")

    # Perform sync from cache to storage
    return provider.sync_folder_to(local_path=cache_path, remote_path=storage_path)

