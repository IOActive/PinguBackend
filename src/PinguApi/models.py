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

# Primary models
from PinguApi.submodels.bot import Bot
from PinguApi.submodels.Job_template import JobTemplate
from PinguApi.submodels.job import Job
from PinguApi.submodels.fuzzer import Fuzzer
from PinguApi.submodels.testcase import TestCase
from PinguApi.submodels.build_metadata import BuildMetadata
from PinguApi.submodels.coverage import Coverage
from PinguApi.submodels.fuzz_target import FuzzTarget
from PinguApi.submodels.fuzz_target_job import FuzzTargetJob
from PinguApi.submodels.statistic import Statistic
from PinguApi.submodels.testcase_variant import TestCaseVariant
from PinguApi.submodels.trial import Trial
from PinguApi.submodels.data_bundle import DataBundle
from PinguApi.submodels.crash import Crash
from PinguApi.submodels.task import Task
from PinguApi.submodels.bot_config import BotConfig
from PinguApi.submodels.project import Project

#Bigquery models
from PinguApi.submodels.fuzzer_stats import FuzzerStats
from PinguApi.submodels.fuzzer_job_run_stats import FuzzerJobRunStats
from PinguApi.submodels.fuzzer_testcase_run_stats import FuzzerTestcaseRunStats
from PinguApi.submodels.crash_stats import  CrashStats
from PinguApi.submodels.corpus_stats import CorpusStats

primary_models= (
    Bot._meta.model_name,
    JobTemplate._meta.model_name,
    Job._meta.model_name,
    Fuzzer._meta.model_name,
    TestCase._meta.model_name,
    FuzzTargetJob._meta.model_name,
    Statistic._meta.model_name,
    TestCaseVariant._meta.model_name,
    Trial._meta.model_name,
    DataBundle._meta.model_name,
    Crash._meta.model_name,
    Task._meta.model_name,
    BotConfig._meta.model_name,
    Project._meta.model_name,
    FuzzTarget._meta.model_name,
    BuildMetadata._meta.model_name,
    Coverage._meta.model_name,
)

bigquery_models = (
    FuzzerStats._meta.model_name,
    FuzzerTestcaseRunStats._meta.model_name,
    FuzzerJobRunStats._meta.model_name,
    CrashStats._meta.model_name,
    CorpusStats._meta.model_name,
)