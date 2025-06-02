import datetime
import json
import yaml
from PinguApi.submodels.project import Project
from src.PinguApi.handlers import storage
from src.PinguApi.utilities import configuration
from PinguApi.submodels.fuzzer_stats import FuzzerStats
from django.utils import timezone

from PinguApi.submodels.fuzz_target import FuzzTarget
from PinguApi.submodels.fuzzer_job_run_stats import FuzzerJobRunStats
from PinguApi.submodels.fuzzer_testcase_run_stats import FuzzerTestcaseRunStats
import logging

logger = logging.getLogger(__name__)

class BigQueryHelper():
    def __init__(self):
        self.monitored_objects = {}
        monitored_projects = Project.objects.all()
        for project in monitored_projects:
            project_id = str(project.id)
            big_query_bucket = configuration.get_bigquery_bucket(yaml.safe_load(project.configuration))
            self.monitored_objects[project_id] = {
                "big_query_bucket": big_query_bucket,
                "fuzzers": []
            }
    
    # Function to insert a path into the tree
    def insert_path(self, path_tree, path):
        parts = path.split('/')
        project = parts[0]
        fuzzer = parts[1]
        job = parts[2]
        kind = parts[3]
        date = parts[4]
        file_name = parts[5]

        # Ensure project level
        if project not in path_tree:
            path_tree[project] = {'fuzzers': []}
            
        project_node = path_tree[project]

        # Find or create fuzzer entry
        fuzzer_node = next((f for f in project_node['fuzzers'] if f['id'] == fuzzer), None)
        if not fuzzer_node:
            fuzzer_node = {'id': fuzzer, 'jobs': []}
            project_node['fuzzers'].append(fuzzer_node)

        # Find or create job entry
        job_node = next((j for j in fuzzer_node['jobs'] if j['id'] == job), None)
        if not job_node:
            job_node = {'id': job, 'kinds': []}
            fuzzer_node['jobs'].append(job_node)

        # Find or create kind entry
        kind_node = next((k for k in job_node['kinds'] if k['name'] == kind), None)
        if not kind_node:
            kind_node = {'name': kind, 'dates': []}
            job_node['kinds'].append(kind_node)

        # Find or create date entry
        date_node = next((d for d in kind_node['dates'] if d['date'] == date), None)
        if not date_node:
            date_node = {'date': date, 'files': []}
            kind_node['dates'].append(date_node)

        # Append file to the date node
        date_node['files'].append(file_name)


    def monitor_project_stats_since_date(self, date):
        try:
            for project_id in list(self.monitored_objects.keys()):  # <-- Iterate over a copy of keys
                payload = self.monitored_objects[project_id]
                iterator = storage.list_blobs(payload['big_query_bucket'], recursive=True)
                for object in iterator:
                    if object['updated'] >= date:
                        self.insert_path(self.monitored_objects, f"{project_id}/{object['name']}")  # Now it's safe!
        except Exception as e:
            pass


    def process_stats(self, stats):
        stats_json = json.loads(stats)
        kind = stats_json['kind']
        timestamp = datetime.datetime.fromtimestamp(stats_json['timestamp'], timezone.get_current_timezone())
        fuzz_target = None
        try:
            fuzz_target = FuzzTarget.objects.get(
                fuzzer=stats_json['fuzzer_id'],
                binary=stats_json['binary'],
                project=stats_json['project_id']
                )
        except Exception as e:
            logger.info("Blackbox stats without fuzztarget")
        
        try:
            fuzzer_stats, created = FuzzerStats.objects.get_or_create(
                project=stats_json['project_id'],
                job=stats_json['job_id'],
                fuzzer=stats_json['fuzzer_id'],
                fuzz_target=fuzz_target.id if fuzz_target else None,
                build_revision = stats_json['build_revision']
            )
        except Exception as e:
            raise Exception("Error creating or getting FuzzerStats object")
        
        match kind:
            case "JobRun":
                try:
                    FuzzerJobRunStats.objects.get_or_create(
                        fuzzer_stats=fuzzer_stats,
                        testcases_executed=int(stats_json['testcases_executed']),
                        new_crashes=int(stats_json['new_crashes']),
                        known_crashes=int(stats_json['known_crashes']),
                        crashes={
                            "crashes":stats_json['crashes']
                        },
                        time=timestamp
                    )
                except Exception as e:
                    raise Exception("Error creating FuzzerJobRunStats object")       
            case 'TestcaseRun':
                try:
                    # Create a new dictionary starting after the `kind` key
                    kind_index = list(stats_json.keys()).index("kind")
                    # Extract fields from "kind" onwards
                    custom_stats = {k: stats_json[k] for k in list(stats_json.keys())[kind_index + 1:]}
                    FuzzerTestcaseRunStats.objects.get_or_create(
                        fuzzer_stats=fuzzer_stats,
                        time=timestamp,
                        custom_stats=custom_stats
                    )
                except Exception as e:
                    raise Exception("Error creating FuzzerTestcaseRunStats object")
                    

    def update_stats_since_date(self, date):
        try:
            # Check timestamp of latest FuzzerStats of the monitored monitored objects
            self.monitor_project_stats_since_date(date)
            
            # Fetch all FuzzerStats included in the monitored_objects dictionary
            for projec_id, payload in self.monitored_objects.items():
                project_fuzzers = payload['fuzzers']
                for fuzzer in project_fuzzers:
                    fuzzer_id = fuzzer['id']
                    fuzzer_jobs = fuzzer['jobs']
                    for job in fuzzer_jobs:
                        job_id = job['id']
                        job_kinds = job['kinds']
                        for kind in job_kinds:
                            kind_name = kind['name']
                            kind_dates = kind['dates']
                            for date in kind_dates:
                                date_str = date['date']
                                date_files = date['files']
                                for file in date_files:
                                    full_object_path = f"{fuzzer_id}/{job_id}/{kind_name}/{date_str}/{file}"
                                    storage_path = f"{payload['big_query_bucket']}/{full_object_path}"
                                    response = storage.read_data(storage_path)
                                    if response:
                                        file_content = response.decode('utf-8')
                                        # Process the file content as needed
                                        self.process_stats(file_content)
        except Exception as e:
            raise Exception(f"Error fetching data from BigQuery")
                                