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
import shutil
from celery import shared_task
from celery.utils.log import get_task_logger
from django.conf import settings
import io
import os


from PinguApi.submodels.project import Project
from PinguApi.handlers.coverage import CoverageHelper
logger = get_task_logger(__name__)

# Coverage Taks 
@shared_task(name="generate_coverage_html_report")
def generate_coverage_html_report(project: Project) -> dict:
    logger.info("Launching coverage report generation Task")
    try:
        # Call the function to generate the HTML report
        helper = CoverageHelper(project)
        result = helper.generate_coverage_report()
        api_url = f"http://{settings.SERVER_HOST}:{settings.SERVER_PORT}/api/coverage/{str(project.id)}/download"
        clean_result = {}
        # clean up coverage related files from result
        for key, value in result.items():
            coverage_report_file = value[0] # fisr position is always the path of the coverage report file
            # store the report to tmp reports folder and set the path to the clean_results map
            html_reports_dir = f"{settings.TMP_FOLDER}/coverage/{str(project.id)}/html_reports/"
            if not os.path.exists(html_reports_dir):
                os.makedirs(html_reports_dir)
            report_path = f"{html_reports_dir}/{key}_report.html"
            shutil.copy(coverage_report_file, report_path)
            clean_result[key] = f"{api_url}/?report={key}_report.html"
                
        logger.info("Coverage report generation Task Completed")
        return clean_result
    
    except Exception as e:
        logger.error(f"Failed to generate coverage report: {e}")
        raise Exception(f"Failed to generate coverage report: {e}")
    
@shared_task(name="get_coverage_artifacts_package")
def get_coverage_artifacts_package(project: Project) -> io.BytesIO:
    try:
        logger.info("Artifacts Package Task Started")
        # Define the path where artifacts are stored
        # Call the function to generate the HTML report
        helper = CoverageHelper(project)
        coverage_package_path = helper.prepare_artifacts_package()

        zip_buffer = io.BytesIO(open(coverage_package_path, 'rb').read())
        
        helper.flush_temporal_coverage_files()
        
        logger.info("Artifacts Package Task Completed")
        return zip_buffer
    except Exception as e:
        raise Exception(f"Failed to generate coverage report")
    
@shared_task(name="get_coverage_html_report")
def get_coverage_html_report(project: Project, report_name):
    try:
        logger.info("Coverage HTML Report Task Started")
        path = f"{settings.TMP_FOLDER}/coverage/{str(project.id)}/html_reports/{report_name}"
        # Define the path where artifacts are stored
        if not os.path.exists(path):
            raise Exception(f"Path does not exist")
        
        return io.BytesIO(open(path, 'rb').read())
        
    except Exception as e:
        logger.error(f"Failed to read coverage report file from path {path}")
        raise Exception(f"Failed to read coverage report file from path {path}")

                                   