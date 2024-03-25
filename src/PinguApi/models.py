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

from django.db import models

# Create your models here.
from PinguApi.submodels.Bot import Bot
from PinguApi.submodels.JobTemplate import JobTemplate
from PinguApi.submodels.Job import Job
from PinguApi.submodels.Fuzzer import Fuzzer
from PinguApi.submodels.TestCase import TestCase
from PinguApi.submodels.BuildMetadata import BuildMetadata
from PinguApi.submodels.Coverage import Coverage
from PinguApi.submodels.FuzzTarget import FuzzTarget
from PinguApi.submodels.FuzzTargetJob import FuzzTargetJob
from PinguApi.submodels.Statistic import Statistic
from PinguApi.submodels.TestCaseVariant import TestCaseVariant
from PinguApi.submodels.Trial import Trial
from PinguApi.submodels.DataBundle import DataBundle
from PinguApi.submodels.Crash import Crash