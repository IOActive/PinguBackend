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

# Create your tasks here
from __future__ import absolute_import, unicode_literals
import base64
import datetime
import shutil

from PinguApi.subtasks.storage.coverage import store_coverage
from PinguApi.subtasks.storage.stats import store_stats
from PinguApi.subtasks.storage.logs import store_logs, download_logs
from PinguApi.subtasks.storage.build import download_build, get_build_list, get_build_size
from PinguApi.subtasks.storage.corpus import store_corpus, download_corpus
from PinguApi.subtasks.storage.blobs import  download_blob, read_blob, write_blob, delete_blob
from PinguApi.subtasks.views.build import upload_build_to_bucket, download_build_from_bucket, remove_build_from_bucket, get_build_from_cache
from PinguApi.subtasks.views.corpus import upload_corpus_to_bucket 
from PinguApi.subtasks.views.logs import download_task_logs
from PinguApi.subtasks.views.fuzzer import upload_fuzzer_to_bucket, download_fuzzer_from_bucket, remove_fuzzer_from_bucket, get_fuzzer_from_cache
from PinguApi.subtasks.views.coverage import generate_coverage_html_report, get_coverage_artifacts_package, get_coverage_html_report
from PinguApi.subtasks.views.custom_binary import upload_custom_binary_to_bucket, download_custom_binary_from_bucket, remove_custom_binary_from_bucket
from PinguApi.subtasks.views.project import create_project_buckets, delete_project_buckets
from PinguApi.subtasks.views.stats import download_and_update_stats
from PinguApi.subtasks.storage.dictionaries import upload_dictionary, download_dictionary, dictionary_exists, list_dictionaries