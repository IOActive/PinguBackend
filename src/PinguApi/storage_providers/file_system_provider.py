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
import json
import os
import shutil
from PinguApi.storage_providers.storage_provider import StorageProvider
from PinguApi.storage_providers.utils import get_bucket_name_and_path
from PinguApi.utilities import shell


class FileSystemProvider(StorageProvider):
    """File system backed storage provider."""

    OBJECTS_DIR = 'objects'
    METADATA_DIR = 'metadata'

    def __init__(self, filesystem_dir):
        self.filesystem_dir = os.path.abspath(filesystem_dir)

    def _get_object_properties(self, bucket, path):
        """Set local object properties."""
        fs_path = self.convert_path(bucket, path)

        data = {
            'bucket': bucket,
            'name': path,
        }

        if not os.path.isdir(fs_path):
            # These attributes only apply to objects, not directories.
            data.update({
                'updated':
                    datetime.datetime.utcfromtimestamp(os.stat(fs_path).st_mtime),
                'size':
                    os.path.getsize(fs_path),
                'metadata':
                    self._get_metadata(bucket, path),
            })

        return data

    def _get_metadata(self, bucket, path):
        """Get the metadata for a given object."""
        fs_metadata_path = self._fs_path(bucket, path, self.METADATA_DIR)
        if os.path.exists(fs_metadata_path):
            with open(fs_metadata_path) as f:
                return json.load(f)

        return {}

    def _fs_bucket_path(self, bucket):
        """Get the local FS path for the bucket."""
        return os.path.join(self.filesystem_dir, bucket)

    def _fs_objects_dir(self, bucket):
        """Get the local FS path for objects in the bucket."""
        return os.path.join(self._fs_bucket_path(bucket), self.OBJECTS_DIR)

    def _fs_path(self, bucket, path, directory):
        """Get the local object/metadata FS path."""
        return os.path.join(self._fs_bucket_path(bucket), directory, path)

    def _write_metadata(self, bucket, path, metadata):
        """Write metadata."""
        if not metadata:
            return

        fs_metadata_path = self.convert_path_for_write(bucket, path,
                                                       self.METADATA_DIR)
        with open(fs_metadata_path, 'w') as f:
            json.dump(metadata, f)

    def convert_path(self, bucket, path, directory=OBJECTS_DIR):
        """Get the local FS path for the remote path."""
        return self._fs_path(bucket, path, directory)

    def convert_path_for_write(self, bucket, path, directory=OBJECTS_DIR):
        """Get the local FS path for writing to the remote path. Creates any
    intermediate directories if necessary (except for the parent bucket
    directory)."""
        if not os.path.exists(self._fs_bucket_path(bucket)):
            raise RuntimeError(
                'Bucket {bucket} does not exist.'.format(bucket=bucket))

        fs_path = self._fs_path(bucket, path, directory)
        shell.create_directory(os.path.dirname(fs_path), create_intermediates=True)

        return fs_path

    def create_bucket(self, name, object_lifecycle, cors):
        """Create a new bucket."""
        bucket_path = self._fs_bucket_path(name)
        if os.path.exists(bucket_path):
            return False

        os.makedirs(bucket_path)
        return True

    def delete_bucket(self, bucketName):
        """Delete a bucket."""
        bucket_path = self._fs_bucket_path(bucketName)
        if not os.path.exists(bucket_path):
            return False

        shutil.rmtree(bucket_path)
        
    def get_bucket(self, name):
        """Get a bucket."""
        bucket_path = self._fs_bucket_path(name)
        if not os.path.exists(bucket_path):
            return None

        return {
            'name': name,
        }

    def _list_files_recursive(self, fs_path):
        """List files recursively."""
        for root, _, filenames in shell.walk(fs_path):
            for filename in filenames:
                yield os.path.join(root, filename)

    def _list_files_nonrecursive(self, fs_path):
        """List files non-recursively."""
        for filename in os.listdir(fs_path):
            yield os.path.join(fs_path, filename)

    def list_blobs(self, target_bucket, recursive=True):
        """List the blobs under the remote path."""
        bucket, path = get_bucket_name_and_path(target_bucket)
        fs_path = self.convert_path(bucket, path)

        if recursive:
            file_paths = self._list_files_recursive(fs_path)
        else:
            file_paths = self._list_files_nonrecursive(fs_path)

        for fs_path in file_paths:
            path = os.path.relpath(fs_path, self._fs_objects_dir(bucket))

            yield self._get_object_properties(bucket, path)

    def copy_file_from(self, target_bucket, local_path):
        """Copy file from  remote path to a local path."""
        bucket, path = get_bucket_name_and_path(target_bucket)
        fs_path = self.convert_path(bucket, path)
        return shell.copy_file(fs_path, local_path)

    def copy_file_to(self, local_path_or_handle, source, metadata=None):
        """Copy file from  local path to a remote path."""
        bucket, path = get_bucket_name_and_path(source)
        fs_path = self.convert_path_for_write(bucket, path)

        if isinstance(local_path_or_handle, str):
            if not shell.copy_file(local_path_or_handle, fs_path):
                return False
        else:
            with open(fs_path, 'wb') as f:
                shutil.copyfileobj(local_path_or_handle, f)

        self._write_metadata(bucket, path, metadata)
        return True

    def sync_folder_from(self, local_path, remote_path):
        bucket, path = get_bucket_name_and_path(remote_path)
        fs_path = self.convert_path(bucket, path)
        return shell.sync_folders(fs_path, local_path)
    
    def sync_folder_to(self, remote_path, local_path):
        bucket, path = get_bucket_name_and_path(remote_path)
        fs_path = self.convert_path(bucket, path)
        return shell.sync_folders(local_path, fs_path)
    
    def copy_blob(self, remote_source, remote_target):
        """Copy a remote file to another remote location."""
        bucket_source, path_source = get_bucket_name_and_path(remote_source)
        fs_source_path = self.convert_path(bucket_source, path_source)

        bucket_target, path_target = get_bucket_name_and_path(remote_target)
        fs_target_path = self.convert_path_for_write(bucket_target, path_target)

        return shell.copy_file(fs_source_path, fs_target_path)

    def read_data(self, source):
        bucket, path = get_bucket_name_and_path(source)
        """Read the data of a remote file."""
        fs_path = self.convert_path(bucket, path)
        if not os.path.exists(fs_path):
            return None

        with open(fs_path, 'rb') as f:
            return f.read()

    def write_data(self, data, target_source, metadata=None):
        """Write the data of a remote file."""
        bucket, path = get_bucket_name_and_path(target_source)
        fs_path = self.convert_path_for_write(bucket, path)
        if isinstance(data, str):
            data = data.encode()

        with open(fs_path, 'wb') as f:
            f.write(data)

        self._write_metadata(bucket, path, metadata)
        return True

    def get(self, source):
        """Get information about a remote file."""
        bucket, path = get_bucket_name_and_path(source)
        fs_path = self.convert_path(bucket, path)
        if not os.path.exists(fs_path):
            return None

        return self._get_object_properties(bucket, path)

    def delete(self, target):
        """Delete a remote file."""
        bucket, path = get_bucket_name_and_path(target)
        fs_path = self.convert_path(bucket, path)
        shell.remove_file(fs_path)

        fs_metadata_path = self.convert_path(bucket, path, self.METADATA_DIR)
        shell.remove_file(fs_metadata_path)
        return True

    def get_storage_file_path(self, bucket, path):
        """Get the full Minio file path."""
        return f"{self.filesystem_dir}/{bucket}/{path}"