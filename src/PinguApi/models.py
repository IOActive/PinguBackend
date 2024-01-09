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