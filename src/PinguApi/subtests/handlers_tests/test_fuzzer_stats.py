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
from unittest.mock import MagicMock, patch
from PinguApi.subtests.views.pingu_api_testcase import PinguAPITestCase
from PinguApi.subtests.views.test_project_api import init_test_project
from PinguApi.subtests.views.test_fuzz_target_api import init_test_FuzzTarget
from PinguApi.subtests.views.test_fuzzer_api import init_test_Fuzzer
from PinguApi.subtests.views.test_job_api import init_test_Job
from rest_framework.authtoken.models import Token
from PinguApi.storage_providers.storage_provider import StorageProvider
from src.PinguApi.handlers.fuzzer_stats import build_results
from django.utils import timezone
from src.PinguApi.handlers.big_query import BigQueryHelper
from minio.helpers import ObjectWriteResult
from PinguApi.submodels.fuzz_target import FuzzTarget
from minio.datatypes import Object


def get_all_file_paths(folder_path: str):
    """Return a list of all file paths in the given folder and subfolders."""
    file_paths = []
    
    # Walk through directory and subdirectories
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_paths.append(os.path.join(root, file))
    
    return file_paths

def init_get_objects_mock(mock_side_effects):
    """Initialize the mock objects for get_object."""
    # Create a mocked ObjectWriteResult object
    for file in get_all_file_paths('src/PinguApi/subtests/test_data/stats'):
        with open(file, 'rb') as f:
            # Read the file content and append it to the list of side effects
            mock_result = MagicMock(spec=ObjectWriteResult)
            mock_result.data = f.read()
            mock_side_effects.append(mock_result)
    
def init_listObjects_mock(mock_objects, project, fuzz_target, job, date, date2=None):
    paths = get_all_file_paths("src/PinguApi/subtests/test_data/stats/")

    for path in paths:
        clean_path = path.split('stats/')[1]
        full_path = f"{project.id}/{fuzz_target.fuzzer.id}_{fuzz_target.binary}/{job.id}/{clean_path}"
        mock_object = Object(
            bucket_name="test-bigquery-buket",
            object_name=full_path,
            last_modified=date
        )
        mock_objects.append(mock_object)
    
    # ADD mock object from 2 day ago
    if date2:
        mock_object_old = Object(
            bucket_name="test-bigquery-buket",
            object_name=f"{project.id}/{fuzz_target.fuzzer.id}_{fuzz_target.binary}/{job.id}/stats/2dayago.json",
            last_modified=date2
            )
        mock_objects.append(mock_object_old)

class TestFuzzerStatsHelper(PinguAPITestCase):
    def setUp(self):
        self.user = self.setup_user()
        self.token = Token.objects.get_or_create(user=self.user)
        self.test_project = init_test_project()
        self.test_job = init_test_Job(self.test_project)
        self.test_job2 = init_test_Job(self.test_project)
        self.test_fuzzer, fuzzer_zip = init_test_Fuzzer(self.test_project)
        self.test_FuzzTarget = init_test_FuzzTarget(self.test_project, fuzzer=self.test_fuzzer)
        
        self.today = datetime.datetime.now(timezone.get_current_timezone())
        self.yesterday = self.today - datetime.timedelta(days=1)
        self.two_days_ago = self.today - datetime.timedelta(days=2)
        self.helper = BigQueryHelper()
        self.mock_objects = []
        init_listObjects_mock(self.mock_objects, self.test_project, self.test_FuzzTarget, self.test_job, self.yesterday, self.two_days_ago)
        self.mock_side_effects = []
        init_get_objects_mock(self.mock_side_effects)
        self.init_stats()
        return super().setUp()
    

    @patch.object(FuzzTarget.objects, 'get')
    @patch.object(StorageProvider, 'list_blobs')
    @patch.object(StorageProvider, 'get')
    def init_stats(self, mock_get_object: MagicMock, mock_listObjects: MagicMock, mock_get: MagicMock):
        mock_listObjects.return_value = self.mock_objects
        mock_get_object.side_effect = self.mock_side_effects
        mock_get.return_value = self.test_FuzzTarget
        
        self.helper.update_stats_since_date(date=self.yesterday)
        
    def test_build_results(self):
        result = build_results(fuzz_target_id=self.test_FuzzTarget.id, group_by='by-job', 
                      start_date=datetime.datetime(2025, 1, 27).strftime("%Y-%m-%d"),
                      end_date=datetime.datetime(2025, 2, 1).strftime("%Y-%m-%d"),
                      interval='1 days')
        expected_output = {
            "cols": [
                {
                    "label": "tests_executed",
                    "type": "number"
                },
                {
                    "label": "new_crashes",
                    "type": "number"
                },
                {
                    "label": "edge_coverage",
                    "type": "number"
                },
                {
                    "label": "avg_exec_per_sec",
                    "type": "number"
                },
                {
                    "label": "fuzzing_time_percent",
                    "type": "number"
                },
                {
                    "label": "new_tests_added",
                    "type": "number"
                },
                {
                    "label": "new_features",
                    "type": "number"
                },
                {
                    "label": "regular_crash_percent",
                    "type": "number"
                },
                {
                    "label": "oom_percent",
                    "type": "number"
                },
                {
                    "label": "leak_percent",
                    "type": "number"
                },
                {
                    "label": "timeout_percent",
                    "type": "number"
                },
                {
                    "label": "startup_crash_percent",
                    "type": "number"
                },
                {
                    "label": "avg_unwanted_log_lines",
                    "type": "number"
                },
                {
                    "label": "total_fuzzing_time_hrs",
                    "type": "number"
                }
            ],
            "rows": [
                {
                    "c": [
                        {
                            "v": 24856.0
                        },
                        {
                            "v": 0.0
                        },
                        {
                            "v": "",
                            "f": "--"
                        },
                        {
                            "v": 0.0
                        },
                        {
                            "v": 0.0
                        },
                        {
                            "v": 48.0
                        },
                        {
                            "v": 75.0
                        },
                        {
                            "v": 100.0
                        },
                        {
                            "v": 0.0
                        },
                        {
                            "v": 0.0
                        },
                        {
                            "v": 0.0
                        },
                        {
                            "v": 0.0
                        },
                        {
                            "v": 2.5
                        },
                        {
                            "v": 0.0
                        }
                    ]
                }
            ],
            "column_descriptions": {}
        }

        assert result == expected_output
        
        result = build_results(fuzz_target_id=self.test_FuzzTarget.id, group_by='by-time', 
                      start_date=datetime.datetime(2025, 1, 27).strftime("%Y-%m-%d"),
                      end_date=datetime.datetime(2025, 2, 1).strftime("%Y-%m-%d"),
                      interval='1 days')
        
        expected_output = {
            "cols": [
                {
                    "label": "tests_executed",
                    "type": "number"
                },
                {
                    "label": "edge_coverage",
                    "type": "number"
                },
                {
                    "label": "avg_exec_per_sec",
                    "type": "number"
                },
                {
                    "label": "fuzzing_time_percent",
                    "type": "number"
                },
                {
                    "label": "new_tests_added",
                    "type": "number"
                },
                {
                    "label": "new_features",
                    "type": "number"
                },
                {
                    "label": "regular_crash_percent",
                    "type": "number"
                },
                {
                    "label": "oom_percent",
                    "type": "number"
                },
                {
                    "label": "leak_percent",
                    "type": "number"
                },
                {
                    "label": "timeout_percent",
                    "type": "number"
                },
                {
                    "label": "startup_crash_percent",
                    "type": "number"
                },
                {
                    "label": "avg_unwanted_log_lines",
                    "type": "number"
                },
                {
                    "label": "total_fuzzing_time_hrs",
                    "type": "number"
                }
            ],
            "rows": [
                {
                    "c": [
                        {
                            "v": 22974.0
                        },
                        {
                            "v": "",
                            "f": "--"
                        },
                        {
                            "v": 0.0
                        },
                        {
                            "v": 0.0
                        },
                        {
                            "v": 48.0
                        },
                        {
                            "v": 75.0
                        },
                        {
                            "v": 100.0
                        },
                        {
                            "v": 0.0
                        },
                        {
                            "v": 0.0
                        },
                        {
                            "v": 0.0
                        },
                        {
                            "v": 0.0
                        },
                        {
                            "v": 0.0
                        },
                        {
                            "v": 0.0
                        }
                    ]
                },
                {
                    "c": [
                        {
                            "v": 207.0
                        },
                        {
                            "v": "",
                            "f": "--"
                        },
                        {
                            "v": 0.0
                        },
                        {
                            "v": 0.0
                        },
                        {
                            "v": 0.0
                        },
                        {
                            "v": 0.0
                        },
                        {
                            "v": 100.0
                        },
                        {
                            "v": 0.0
                        },
                        {
                            "v": 0.0
                        },
                        {
                            "v": 0.0
                        },
                        {
                            "v": 0.0
                        },
                        {
                            "v": 0.0
                        },
                        {
                            "v": 0.0
                        }
                    ]
                },
                {
                    "c": [
                        {
                            "v": 4.0
                        },
                        {
                            "v": "",
                            "f": "--"
                        },
                        {
                            "v": 0.0
                        },
                        {
                            "v": 0.0
                        },
                        {
                            "v": 0.0
                        },
                        {
                            "v": 0.0
                        },
                        {
                            "v": 100.0
                        },
                        {
                            "v": 0.0
                        },
                        {
                            "v": 0.0
                        },
                        {
                            "v": 0.0
                        },
                        {
                            "v": 0.0
                        },
                        {
                            "v": 10.0
                        },
                        {
                            "v": 0.0
                        }
                    ]
                },
                {
                    "c": [
                        {
                            "v": 1671.0
                        },
                        {
                            "v": "",
                            "f": "--"
                        },
                        {
                            "v": 0.0
                        },
                        {
                            "v": 0.0
                        },
                        {
                            "v": 0.0
                        },
                        {
                            "v": 0.0
                        },
                        {
                            "v": 100.0
                        },
                        {
                            "v": 0.0
                        },
                        {
                            "v": 0.0
                        },
                        {
                            "v": 0.0
                        },
                        {
                            "v": 0.0
                        },
                        {
                            "v": 0.0
                        },
                        {
                            "v": 0.0
                        }
                    ]
                }
            ],
            "column_descriptions": {}
        }
        
        assert result == expected_output