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
import django
from django.test.utils import setup_databases, setup_test_environment

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PinguBackend.settings.development')  # replace with your project name
django.setup()
#if os.getcwd().split('/')[-1] != 'src':
#    os.chdir(os.getcwd()+'/src')