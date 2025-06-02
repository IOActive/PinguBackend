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

import unittest
import yaml
from src.PinguApi.utilities.configuration import replace_test_prefix, get_all_buckets, get_value

class TestReplaceTestPrefix(unittest.TestCase):
    
    def setUp(self):
        
        # Sample YAML content as a dictionary
        self.sample_yaml = {
            "blobs": {
                "bucket": "test-blobs-bucket"
            },
            "deployment": {
                "bucket": "test-deployment-bucket"
            },
            "build":{
              "release":{
                  "bucket": "test-release-bucket"
              }  
            },
            "env": {
                "APPLICATION_ID": "test",
                "PROJECT_NAME": "test-project"
            }
            
        }
    
    def test_get_all_buckets(self):
        expected_output = ["test-blobs-bucket", "test-deployment-bucket", "test-release-bucket"]
        buckets = get_all_buckets(self.sample_yaml)
        # Assert that the result matches the expected output
        self.assertEqual(buckets, expected_output)
        
    def test_replace_test_prefix(self):
        # Expected output after replacing 'test-' with a new prefix
        expected_output = {
            "blobs": {
                "bucket": "new-prefix-blobs-bucket"
            },
            "build":{
              "release":{
                  "bucket": "new-prefix-release-bucket"
              }  
            },
            "deployment": {
                "bucket": "new-prefix-deployment-bucket"
            },            
            "env": {
                "APPLICATION_ID": "test",
                "PROJECT_NAME": "new-prefix-project"
            }
        }
        
        # Call the function with the sample YAML and a new prefix
        result = replace_test_prefix(self.sample_yaml, 'new-prefix-')
        
        # Convert the result back to a string for comparison
        result_str = yaml.dump(result)
        expected_output_str = yaml.dump(expected_output)
        
        # Assert that the result matches the expected output
        self.assertEqual(result_str, expected_output_str)
        
    def test_get_value(self):
        expected_value = "test-deployment-bucket"
        value = get_value(self.sample_yaml, "deployment.bucket")
        self.assertEqual(value, expected_value)
