import os
import datetime
from django.db import transaction

from scripts.load_config_to_env import load_config_env


# load backend component configuration into enviroment context
load_config_env("config/system/config.yaml")
load_config_env("config/redis/config.yaml")
load_config_env("config/database/config.yaml")
load_config_env("config/minio/config.yaml")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PinguBackend.settings.development")
import django
django.setup()

from PinguApi.submodels.fuzzer import Fuzzer
from PinguApi.submodels.Job_template import JobTemplate

LIBFUZZER_TEMPLATE = """MAX_FUZZ_THREADS = 1
MAX_TESTCASES = 2
FUZZ_TEST_TIMEOUT = 8400
TEST_TIMEOUT = 65
WARMUP_TIMEOUT = 65
BAD_BUILD_CHECK = False
THREAD_ALIVE_CHECK_INTERVAL = 1
REPORT_OOMS_AND_HANGS = True
CORPUS_FUZZER_NAME_OVERRIDE = libFuzzer
ENABLE_GESTURES = False
THREAD_DELAY = 30.0
"""

AFL_TEMPLATE = """MAX_FUZZ_THREADS = 1
MAX_TESTCASES = 2
FUZZ_TEST_TIMEOUT = 8400
TEST_TIMEOUT = 30
WARMUP_TIMEOUT = 30
BAD_BUILD_CHECK = False
THREAD_ALIVE_CHECK_INTERVAL = 1
CORPUS_FUZZER_NAME_OVERRIDE = libFuzzer
ADDITIONAL_PROCESSES_TO_KILL = afl-fuzz afl-showmap
ENABLE_GESTURES = False
THREAD_DELAY  = 30.0
"""

TEMPLATES = {
    "libFuzzer": LIBFUZZER_TEMPLATE,
    "afl": AFL_TEMPLATE,
}

def setup_fuzzers():
    """Set up fuzzers."""
    fuzzers = [
        {
            "name": "libFuzzer",
            "revision": 1,
            "file_size": 0,
            "source": "builtin",
            "builtin": True,
            "stats_column_descriptions": '''fuzzer: "Fuzz target"
tests_executed: "Number of testcases executed during this time period"
new_crashes: "Number of new unique crashes observed during this time period"
edge_coverage: "Coverage for this fuzz target (number of edges/total)"
cov_report: "Link to coverage report"
corpus_size: "Size of the minimized corpus generated based on code coverage (number of testcases and total size on disk)"
avg_exec_per_sec: "Average number of testcases executed per second"
fuzzing_time_percent: "Percent of expected fuzzing time that is actually spent fuzzing."
new_tests_added: "New testcases added to the corpus during fuzzing based on code coverage"
new_features: "New coverage features based on new tests added to corpus."
regular_crash_percent: "Percent of fuzzing runs that had regular crashes (other than ooms, leaks, timeouts, startup and bad instrumentation crashes)"
oom_percent: "Percent of fuzzing runs that crashed on OOMs (should be 0)"
leak_percent: "Percent of fuzzing runs that crashed on memory leaks (should be 0)"
timeout_percent: "Percent of fuzzing runs that had testcases timeout (should be 0)"
startup_crash_percent: "Percent of fuzzing runs that crashed on startup (should be 0)"
avg_unwanted_log_lines: "Average number of unwanted log lines in fuzzing runs (should be 0)"
total_fuzzing_time_hrs: "Total time in hours for which the fuzzer(s) ran. Will be lower if fuzzer hits a crash frequently."
logs: "Link to fuzzing logs"
corpus_backup: "Backup copy of the minimized corpus generated based on code coverage"''',
            "stats_columns": """sum(t.number_of_executed_units) as tests_executed,
max(j.new_crashes) as new_crashes,
_EDGE_COV as edge_coverage,
_COV_REPORT as cov_report,
_CORPUS_SIZE as corpus_size,
avg(t.average_exec_per_sec) as avg_exec_per_sec,
avg(t.fuzzing_time_percent) as fuzzing_time_percent,
sum(t.new_units_added) as new_tests_added,
sum(t.new_features) as new_features,
avg(t.crash_count*100) as regular_crash_percent,
avg(t.oom_count*100) as oom_percent,
avg(t.leak_count*100) as leak_percent,
avg(t.timeout_count*100) as timeout_percent,
avg(t.startup_crash_count*100) as startup_crash_percent,
avg(t.log_lines_unwanted) as avg_unwanted_log_lines,
sum(t.actual_duration/3600.0) as total_fuzzing_time_hrs,
_FUZZER_RUN_LOGS as logs,
_CORPUS_BACKUP as corpus_backup,""",
            "timestamp": datetime.datetime.now(),
        },
        {
            "name": "afl",
            "revision": 1,
            "file_size": 0,
            "source": "builtin",
            "builtin": True,
            "stats_column_descriptions": '''fuzzer: "Fuzz target"
new_crashes: "Number of new unique crashes observed during this time period"
edge_coverage: "Edge coverage for this fuzz target (number of edges / total)"
cov_report: "Link to coverage report"
corpus_size: "Size of the minimized corpus generated based on code coverage (number of testcases and total size on disk)"
avg_exec_per_sec: "Average number of testcases executed per second"
stability: "Percentage of edges that behave deterministically"
new_tests_added: "New testcases added to the corpus during fuzzing based on code coverage"
regular_crash_percent: "Percent of fuzzing runs that had regular crashes (other than startup and bad instrumentation crashes)"
timeout_percent: "Percent of fuzzing runs that had testcases timeout (should be 0)"
startup_crash_percent: "Percent of fuzzing runs that crashed on startup (should be 0)"
avg_unwanted_log_lines: "Average number of unwanted log lines in fuzzing runs (should be 0)"
total_fuzzing_time_hrs: "Total time in hours for which the fuzzer(s) ran. Will be lower if fuzzer hits a crash frequently."
logs: "Link to fuzzing logs"
corpus_backup: "Backup copy of the minimized corpus generated based on code coverage"''',
            "stats_columns": """custom(j.new_crashes) as new_crashes,
_EDGE_COV as edge_coverage,
_COV_REPORT as cov_report,
_CORPUS_SIZE as corpus_size,
avg(t.average_exec_per_sec) as avg_exec_per_sec,
avg(t.stability) as stability,
sum(t.new_units_added) as new_tests_added,
avg(t.crash_count*100) as regular_crash_percent,
avg(t.timeout_count*100) as timeout_percent,
avg(t.startup_crash_count*100) as startup_crash_percent,
avg(t.log_lines_unwanted) as avg_unwanted_log_lines,
sum(t.actual_duration/3600.0) as total_fuzzing_time_hrs,
_FUZZER_RUN_LOGS as logs,
_CORPUS_BACKUP as corpus_backup,""",
            "timestamp": datetime.datetime.now(),
        },
    ]

    for fuzzer_data in fuzzers:
        fuzzer, created = Fuzzer.objects.get_or_create(
            name=fuzzer_data["name"],
            defaults=fuzzer_data,
        )
        if created:
            print(f"Created fuzzer: {fuzzer.name}")
        else:
            print(f"Fuzzer already exists: {fuzzer.name}")


def setup_templates():
    """Set up job templates."""
    for name, template in TEMPLATES.items():
        job_template, created = JobTemplate.objects.get_or_create(
            name=name,
            defaults={"environment_string": template},
        )
        if created:
            print(f"Created job template: {job_template.name}")
        else:
            print(f"Job template already exists: {job_template.name}")


if __name__ == "__main__":
    with transaction.atomic():
        setup_fuzzers()
        setup_templates()
