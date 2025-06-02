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

import hashlib
import logging
import os
import shutil
import time
from urllib.parse import urlparse
import random
import ast

from PinguApi.utilities import shell

logger = logging.getLogger(__name__)

FAIL_WAIT = 0
FAIL_RETRIES = 1


def read_data_from_file(file_path, eval_data=True, default=None):
    """Returns eval-ed data from pingu_sdk.file."""
    if not os.path.exists(file_path):
        return default

    failure_wait_interval = FAIL_WAIT
    file_content = None
    retry_limit = FAIL_RETRIES
    for _ in range(retry_limit):
        try:
            with open(file_path, "rb") as file_handle:
                file_content = file_handle.read()
        except Exception as e:
            file_content = None
            logger.warning("Error occurred while reading %s, retrying." % file_path)
            time.sleep(random.uniform(1, failure_wait_interval))
            continue

    if file_content is None:
        logger.error("Failed to read data from pingu_sdk.file %s." % file_path)
        return None

    if not eval_data:
        return file_content

    if not file_content:
        return default

    try:
        return ast.literal_eval(file_content.decode("utf-8"))
    except (SyntaxError, TypeError):
        return None


def write_data_to_file(content, file_path, append=False):
    """Writes data to file."""
    failure_wait_interval = FAIL_WAIT
    file_mode = "ab" if append else "wb"
    retry_limit = FAIL_RETRIES

    for _ in range(retry_limit + 1):
        try:
            with open(file_path, file_mode) as file_handle:
                file_handle.write(content)
        except TypeError:
            # If we saw a TypeError, content was not bytes-like. Convert it.
            content = str(content).encode("utf-8")
            continue
        except EnvironmentError:
            # An EnvironmentError signals a problem writing the file. Retry in case
            # it was a spurious error.
            logger.warning("Error occurred while writing %s, retrying." % file_path)
            time.sleep(random.uniform(1, failure_wait_interval))
            continue

        # Successfully written data file.
        return

    logger.error("Failed to write data to file %s." % file_path)


def string_hash(obj):
    """Returns a SHA-1 hash of the object."""
    return hashlib.sha256(str(obj).encode("utf-8")).hexdigest()


def remove_prefix(string, prefix):
    """Strips the prefix from pingu_sdk.a string."""
    if string.startswith(prefix):
        return string[len(prefix) :]

    return string


def get_directory_hash_for_path(file_path):
    """Return the directory hash for a file path (excludes file name)."""
    root_directory = os.getcwd()
    directory_path = os.path.dirname(file_path)
    normalized_directory_path = remove_prefix(directory_path, root_directory + os.sep)
    normalized_directory_path = normalized_directory_path.replace("\\", "/")
    return string_hash(normalized_directory_path)


def get_bucket_name_and_path(cloud_storage_file_path):
    """Return bucket name and path given a full cloud storage path."""
    schema, _ = get_schema_and_domain(cloud_storage_file_path)
    if schema:
        bucket_name_and_path = remove_scheme(cloud_storage_file_path)
    else:
        bucket_name_and_path = cloud_storage_file_path

    if bucket_name_and_path[0] == "/":
        bucket_name_and_path = bucket_name_and_path.split("/", 1)[1]

    if "/" in bucket_name_and_path:
        bucket_name, path = bucket_name_and_path.split("/", 1)
        if "(" in path:
            path = path.split("(", 1)[0]
    else:
        bucket_name = bucket_name_and_path
        path = ""

    return bucket_name, path


def get_schema_and_domain(url):
    """Extracts the schema (protocol) and domain from  URL, if present."""
    try:
        # Parse the URL
        parsed_url = urlparse(url)

        # Extract the schema (e.g., 'http', 'https', 'gs', 's3')
        schema = parsed_url.scheme

        # Extract the domain (e.g., 'example.com') if present
        domain = parsed_url.netloc if parsed_url.scheme in ["http", "https"] else None

        return (schema, f"{domain}/")
    except Exception as e:
        print("Failed to parse URL:", e)
        return None, url


def remove_scheme(bucket_path):
    """Remove scheme (and domain for HTTP/HTTPS) from the bucket path."""
    if "://" not in bucket_path:
        raise Exception("Invalid bucket path: " + bucket_path)

    # Parse the URL
    parsed_url = urlparse(bucket_path)

    # If it's HTTP/HTTPS, return only the path after the domain
    if parsed_url.scheme in ["http", "https"]:
        return parsed_url.path.lstrip("/")  # Remove leading slash if any

    # Otherwise, return the path after the scheme (e.g., for gs://, s3://)
    return f"{parsed_url.netloc}{parsed_url.path}"


def file_hash(file_path):
    """Returns the SHA-256 hash of |file_path| contents."""
    chunk_size = 51200  # Read in 50 KB chunks.
    digest = hashlib.sha256()
    with open(file_path, 'rb') as file_handle:
        chunk = file_handle.read(chunk_size)
        while chunk:
            digest.update(chunk)
            chunk = file_handle.read(chunk_size)

    return digest.hexdigest()

def legalize_filenames(file_paths):
    """Convert the name of every file in |file_paths| a name that is legal on
  Windows. Returns list of legally named files."""

    illegal_chars = {'<', '>', ':', '\\', '|', '?', '*'}
    failed_to_move_files = []
    legally_named = []
    for file_path in file_paths:
        file_dir_path, basename = os.path.split(file_path)
        if not any(char in illegal_chars for char in basename):
            legally_named.append(file_path)
            continue

        # Hash file to get new name since it also lets us get rid of duplicates,
        # will not cause collisions for different files and makes things more
        # consistent (since libFuzzer uses hashes).
        sha1sum = file_hash(file_path)
        new_file_path = os.path.join(file_dir_path, sha1sum)
        try:
            shutil.move(file_path, new_file_path)
            legally_named.append(new_file_path)
        except OSError:
            failed_to_move_files.append((file_path, new_file_path))
    if failed_to_move_files:
        logger.error(
            'Failed to rename files.', failed_to_move_files=failed_to_move_files)

    return legally_named


def legalize_storage_files(directory):
    """Convert the name of every corpus file in |directory| to a name that is
  allowed on Windows."""
    # Iterate through return value of legalize_filenames to convert every
    # filename.
    files_list = shell.get_files_list(directory)
    legalize_filenames(files_list)