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

class StorageProvider(object):
    """Core storage provider interface."""

    def create_bucket(self, name, object_lifecycle, cors):
        """Create a new bucket."""
        raise NotImplementedError

    def delete_bucket(self, name):
        """Delete a bucket."""
        raise NotImplementedError

    def get_bucket(self, name):
        """Get a bucket."""
        raise NotImplementedError

    def list_blobs(self, remote_path, recursive=True):
        """List the blobs under the remote path."""
        raise NotImplementedError

    def copy_file_from(self, remote_path, local_path):
        """Copy file from  remote path to a local path."""
        raise NotImplementedError

    def copy_file_to(self, local_path_or_handle, remote_path, metadata=None):
        """Copy file from  local path to a remote path."""
        raise NotImplementedError

    def copy_blob(self, remote_source, remote_target):
        """Copy a remote file to another remote location."""
        raise NotImplementedError

    def read_data(self, remote_path):
        """Read the data of a remote file."""
        raise NotImplementedError

    def write_data(self, data, remote_path, metadata=None):
        """Write the data of a remote file."""
        raise NotImplementedError

    def get(self, remote_path):
        """Get information about a remote file."""
        raise NotImplementedError

    def delete(self, remote_path):
        """Delete a remote file."""
        raise NotImplementedError
    
    def get_storage_path(bucket, path):
        raise NotImplemented
    
    def sync_folder_from(self, local_path, remote_path, delete=False):
        raise NotImplemented

    def sync_folder_to(self, remote_path, local_path, metadata='', delete=False):
        raise NotImplemented
