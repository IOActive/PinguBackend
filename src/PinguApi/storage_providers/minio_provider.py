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
import io
import os
from pathlib import Path
from minio import Minio, S3Error
from minio.commonconfig import CopySource
from urllib3.exceptions import ResponseError
from PinguApi.storage_providers.storage_provider import StorageProvider
import logging
from PinguApi.storage_providers.utils import get_bucket_name_and_path

logger = logging.getLogger(__name__)


class MinioProvider(StorageProvider):
    """Minio storage provider."""

    def __init__(self, host, access_key, secret_key) -> None:
        super().__init__()
        self.host = host
        try:
            self.client = Minio(
                host, access_key=access_key, secret_key=secret_key, secure=False
            )
        except Exception as e:
            raise Exception('Minio client connection failed')

    def create_bucket(self, name, object_lifecycle=None, cors=None):
        """Create a new bucket."""
        project_id = name
        try:
            self.client.make_bucket(project_id, object_lock=True)
        except S3Error as e:
            logger.warning("Failed to create bucket %s: %s" % (name, e))
            raise

        return True

    def get_bucket(self, name):
        """Get a bucket."""
        target_bucket = None
        try:
            buckets = self.client.list_buckets()
            for bucket in buckets:
                if bucket.name == name:
                    target_bucket = bucket
            return target_bucket
        except S3Error as e:
            raise e

    def list_blobs(self, remote_path, recursive=True):
        """List the blobs under the remote path."""
        bucket_name, path = get_bucket_name_and_path(remote_path)
        properties = {}

        if recursive:
            # List objects information recursively.
            objects = self.client.list_objects(bucket_name, prefix=path, recursive=True)
            for obj in objects:
                properties["bucket"] = obj.bucket_name
                properties["name"] = obj.object_name
                properties["updated"] = obj.last_modified
                properties["size"] = obj.size
                yield properties

        if not recursive:
            # When doing delimiter listings, the "directories" will be in `prefixes`.
            objects = self.client.list_objects(bucket_name, prefix=path)
            for obj in objects:
                properties["bucket"] = obj.bucket_name
                properties["name"] = obj.object_name
                yield properties

    def copy_file_from(self, remote_path, local_path):
        """Copy file from  remote path to a local path."""
        bucket_name, path = get_bucket_name_and_path(remote_path)

        try:
            # Download data of an object.
            blob = self.client.fget_object(bucket_name, path, local_path)
            logger.info(
                "downloaded {0} object; etag: {1}, version-id: {2}".format(
                    blob.object_name, blob.etag, blob.version_id
                )
            )
        except S3Error as e:
            logger.warning(
                "Failed to copy cloud storage file %s to local file %s."
                % (remote_path, local_path)
            )

            raise

        return True

    def sync_folder_from(self, local_path, remote_path, delete=True):
        """Copy file from remote path to a local path."""
        bucket_name, path = get_bucket_name_and_path(remote_path)

        try:
            existing_files = set()
            # Download data of an object.
            for item in self.client.list_objects(
                bucket_name, prefix=path, recursive=True
            ):
                local_file_path = os.path.join(local_path, os.path.basename(item.object_name))
                self.copy_file_from(f"{bucket_name}/{item.object_name}", local_file_path)
                existing_files.add(local_file_path)
                logger.info(
                    "downloaded {0} object; etag: {1}, version-id: {2}".format(
                        item.object_name, item.etag, item.version_id
                    )
                )
            if delete:
                for root, _, files in os.walk(local_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        if file_path not in existing_files:
                            os.remove(file_path)
                            logger.info(f"Deleted local file {file_path}")
        except S3Error as e:
            logger.warning(
                "Failed to copy cloud storage file %s to local file %s."
                % (remote_path, local_path)
            )
            raise

        return True

    def sync_folder_to(self, remote_path, local_path, metadata="", delete=False):
        try:
            existing_files = set()
            for path in Path(local_path).rglob("*"):
                if os.path.isfile(path):
                    remote_file_path = f"{remote_path}{path.relative_to(local_path)}"
                    self.copy_file_to(
                        str(path), remote_file_path, metadata, size=path.stat().st_size
                    )
                    bucket_path, remote_file_path = get_bucket_name_and_path(remote_file_path)
                    existing_files.add(remote_file_path)
            if delete:
                bucket_name, remote_dir_path = get_bucket_name_and_path(remote_path)
                for obj in self.client.list_objects(bucket_name, prefix=remote_dir_path, recursive=True):
                    remote_file_path = f"{obj.object_name}"
                    if remote_file_path not in existing_files:
                        self.client.remove_object(bucket_name, obj.object_name)
                        logger.info(f"Deleted remote file {obj.object_name}")
            return True
        except Exception as e:
            logger.warning("Failed to sync folder %s to cloud storage." % local_path)
            raise

    def copy_file_to(self, local_path_or_handle, remote_path, metadata=None, size=None):
        """Copy file from local path to a remote path."""
        bucket_name, path = get_bucket_name_and_path(remote_path)

        try:
            if metadata:
                if isinstance(local_path_or_handle, str):
                    # Upload data with metadata.
                    blob = self.client.fput_object(
                        bucket_name,
                        path,
                        local_path_or_handle,
                        metadata=metadata,
                    )
                elif isinstance(local_path_or_handle, io.IOBase):
                    # Upload data with metadata.
                    blob = self.client.put_object(
                        bucket_name,
                        path,
                        io.BytesIO(local_path_or_handle.read()),
                        length=size,
                        metadata=metadata,
                    )
                else:
                    raise TypeError("local_path_or_handle must be a string or file-like object")
                logger.info(
                    "created {0} object; etag: {1}, version-id: {2}".format(
                        blob.object_name, blob.etag, blob.version_id
                    )
                )
            else:
                if isinstance(local_path_or_handle, str):
                    # Upload data with metadata.
                    blob = self.client.fput_object(
                        bucket_name, path, local_path_or_handle
                    )
                elif isinstance(local_path_or_handle, io.IOBase):
                    # Upload data with metadata.
                    blob = self.client.put_object(
                        bucket_name=bucket_name, 
                        object_name=path, 
                        data=io.BytesIO(local_path_or_handle.read()),
                        length=size
                    )
                else:
                    raise TypeError("local_path_or_handle must be a string or file-like object")
                logger.info(
                    "created {0} object; etag: {1}, version-id: {2}".format(
                        blob.object_name, blob.etag, blob.version_id
                    )
                )
        except S3Error as e:
            logger.warning(
                "Failed to copy local file %s to cloud storage file %s."
                % (local_path_or_handle, remote_path)
            )
            raise
        except OSError as e:
            logger.warning(
                "Failed to read local file %s." % (local_path_or_handle,)
            )
            raise
        except Exception as e:
            logger.warning("Failed to copy local file %s to cloud storage file %s." % (local_path_or_handle, remote_path))
            raise

        return True

    def copy_blob(self, remote_source, remote_target):
        """Copy a remote file to another remote location."""
        source_bucket_name, source_path = get_bucket_name_and_path(remote_source)
        target_bucket_name, target_path = get_bucket_name_and_path(remote_target)

        try:
            # copy an object from  bucket to another.
            blob = self.client.copy_object(
                target_bucket_name,
                target_path,
                CopySource(source_bucket_name, source_path),
            )
            logger.info(
                "copied {0} object; etag: {1}, version-id: {2}".format(
                    blob.object_name, blob.etag, blob.version_id
                )
            )
        except S3Error as e:
            logger.warning(
                "Failed to copy cloud storage file %s to cloud storage "
                "file %s." % (remote_source, remote_target)
            )
            raise

        return True

    def read_data(self, remote_path):
        """Read the data of a remote file."""
        bucket_name, path = get_bucket_name_and_path(remote_path)

        try:
            http_response = self.client.get_object(bucket_name, path)
            return http_response.data
        except ResponseError as e:
            logger.warning("Failed to read cloud storage file %s." % remote_path)
            raise
        finally:
            http_response.close()
            http_response.release_conn()

    def write_data(self, data, remote_path, metadata=None):
        """Write the data of a remote file."""
        bucket_name, path = get_bucket_name_and_path(remote_path)

        try:
            if type(data) is not bytes:
                data = data.encode()
            result = self.client.put_object(
                bucket_name,
                path,
                io.BytesIO(data),
                len(data),
                metadata=metadata,
            )
            logger.info(
                "created {0} object; etag: {1}, version-id: {2}".format(
                    result.object_name,
                    result.etag,
                    result.version_id,
                ),
            )
        except S3Error:
            logger.warning("Failed to write cloud storage file %s." % remote_path)
            raise
        except Exception as e:
            logger.error("Failed to upload blob")
            raise

        return True

    def get(self, remote_path):
        """Get information about a remote file."""
        bucket, path = get_bucket_name_and_path(remote_path)
        data = {
            "bucket": bucket,
            "name": path,
        }

        try:
            result = self.client.stat_object(bucket, path)
            logger.info(
                "last-modified: {0}, size: {1}".format(
                    result.last_modified,
                    result.size,
                ),
            )
            data.update(
                {
                    "updated": result.last_modified,
                    "size": result.size,
                    "metadata": result.metadata,
                }
            )
            return data
        except S3Error as e:
            if e.code == "NoSuchKey":
                return None
            else:
                raise

    def delete(self, remote_path):
        """Delete a remote file."""
        bucket_name, path = get_bucket_name_and_path(remote_path)

        try:
            # Remove object.
            self.client.remove_object(bucket_name, path)
        except S3Error:
            logger.warning("Failed to delete cloud storage file %s." % remote_path)
            raise

        return True

    def get_storage_path(self, bucket, path):
        """Get the full Minio file path."""
        return f"http://{self.host}/{bucket}/{path}"

    def delete_bucket(self, bucketName):
        self.client.remove_bucket(bucketName)