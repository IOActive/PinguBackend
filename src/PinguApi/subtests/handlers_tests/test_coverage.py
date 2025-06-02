import datetime
import os
import subprocess
import unittest
from unittest.mock import MagicMock, Mock, patch
from uuid import uuid4
from pyfakefs import fake_filesystem_unittest
from minio.helpers import ObjectWriteResult
from PinguApi.handlers.coverage import CoverageHelper
from minio.datatypes import Object

from PinguApi.handlers import storage
from PinguApi.utilities import configuration

class CoverageHandlerTest(fake_filesystem_unittest.TestCase):
    def setUp(self):
        self.setUpPyfakefs()
        self.cache_folder = '/tmp/cache/5bb61f99096029865b5da36f1e867350b452e32e666aa4c2c877a7a0cbd4936c'
        self.cache_global_folder = '/tmp/cache/e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'
        self.fs.create_dir(self.cache_folder)
        self.fs.create_dir(f"{self.cache_folder}/output")
        self.fs.add_real_directory(source_path='src/PinguApi/subtests/test_data/coverage/inputs',
                                   read_only=False,
                                   target_path=self.cache_folder)
        self.fuzzer_name = 'libFuzzer_cov_fuzzer'
        self.project_id = uuid4()
        self.init_listObjects_mock()
        self.init_get_objects_mock()
        return super().setUp()
    
    def get_all_file_paths(self, folder_path: str):
        """Return a list of all file paths in the given folder and subfolders."""
        file_paths = []
        
        # Walk through directory and subdirectories
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_paths.append(os.path.join(root, file))
        
        return file_paths
    
    def init_get_objects_mock(self):
        """Initialize the mock objects for get_object."""
        # Create a mocked ObjectWriteResult object
        
        self.mock_side_effects = []
        for file in self.get_all_file_paths(self.cache_folder):
            with open(file, 'rb') as f:
                # Read the file content and append it to the list of side effects
                mock_result = MagicMock(spec=ObjectWriteResult)
                mock_result.data = f.read()
                self.mock_side_effects.append(mock_result)
        

    def init_listObjects_mock(self):
        paths = self.get_all_file_paths("/")
        self.mock_objects = []

        for path in paths:
            mock_object = {
                "bucket": "test-coverage-bucket",
                "name": f"{self.fuzzer_name}/{os.path.basename(path)}",
                "updated": datetime.datetime.now(),
                "size": 1234
            }
            self.mock_objects.append(mock_object)
            
    def subprocess_side_effect(self):
        yield self.fs.add_real_file(
            source_path="src/PinguApi/subtests/test_data/coverage/coverage.profdata",
            read_only=True,
            target_path=f"{self.cache_folder}/coverage.profdata"
        )

        yield subprocess.CompletedProcess(
            args=["ls", "-l"],
            returncode=0,  # Simula éxito
            stdout="Fake Coverage data",
            stderr=""
        )
 

        yield None  # Third call - does nothing

        yield self.fs.add_real_file(
            source_path="src/PinguApi/subtests/test_data/coverage/report.html",
            read_only=True,
            target_path=f"{self.cache_folder}/output/report.html"
        )

        # Second batch of subprocess calls
        yield self.fs.add_real_file(
            source_path="src/PinguApi/subtests/test_data/coverage/coverage.profdata",
            read_only=True,
            target_path=f"{self.cache_global_folder}/coverage.profdata"
        )

        yield subprocess.CompletedProcess(
            args=['echo', 'hello'],
            returncode=0,  # Simula éxito
            stdout="Fake Coverage data",
            stderr=""
        )

        yield None  # Third call in this batch - does nothing

        yield self.fs.add_real_file(
            source_path="src/PinguApi/subtests/test_data/coverage/report.html",
            read_only=True,
            target_path=f"{self.cache_global_folder}/output/report.html"
        )
        

    @patch('PinguApi.handlers.coverage.configuration.get_coverage_bucket')
    @patch('yaml.safe_load')
    @patch.object(storage, 'copy_file_from')
    @patch.object(storage, 'list_blobs')
    @patch('magic.from_file')
    @patch('subprocess.run')
    def test_generate_coverage_report(self, 
                                    mock_subprocess_run: MagicMock, 
                                    mock_magic_from_file: MagicMock, 
                                    mock_listObjects: MagicMock, 
                                    mock_copy_file_from: MagicMock, 
                                    mock_safe_load: MagicMock, 
                                    mock_get_coverage_bucket: MagicMock):
        # Mock the subprocess call to simulate coverage report generation
        effects = self.subprocess_side_effect()
        mock_subprocess_run.side_effect = lambda *args, **kwargs: next(effects)
        
        mock_listObjects.return_value = self.mock_objects
        mock_copy_file_from.side_effect = self.mock_side_effects
        
        mock_magic_from_file.return_value = "application/x-executable"
        
        mock_get_coverage_bucket.return_value = 'test-coverage-bucket'
        
        # Create a mock project object
        project = Mock()

        # Mock the configuration attribute
        project.configuration = Mock()
        project.id = self.project_id
        
        settings = Mock()
        settings.TMP_FOLDER = 'tmp'
        
        helper = CoverageHelper(project)    
        result = helper.generate_coverage_report()
        
        report_path , coverage_files = result[f'{self.fuzzer_name}']
        
        assert report_path == f'.{self.cache_folder}/output/report.html'
        
        assert os.path.exists(report_path)
        
        assert os.path.getsize(report_path) > 0
        
        assert coverage_files == [
            f'{self.cache_folder}/1740399073.profraw',
            f'{self.cache_folder}/1740399090.profraw',
            f'{self.cache_folder}/1740399178.profraw',
            f'{self.cache_folder}/1740399162.profraw',
            f'.{self.cache_folder}/cov_fuzzer']
        
        final_report_path, final_coverage_files =  result[f'global']
        assert final_report_path == f'.{self.cache_global_folder}//output/report.html'
        
        helper.flush_temporal_coverage_files()
        
        assert os.listdir(f"tmp/cache/5bb61f99096029865b5da36f1e867350b452e32e666aa4c2c877a7a0cbd4936c") == []
        
    
    @patch('PinguApi.handlers.coverage.configuration.get_coverage_bucket')
    @patch('yaml.safe_load')
    @patch.object(storage, 'copy_file_from')
    @patch.object(storage, 'list_blobs')
    def test_download_coverage(self,
                                mock_listObjects: MagicMock, 
                                mock_copy_file_from: MagicMock, 
                                mock_safe_load: MagicMock, 
                                mock_get_coverage_bucket: MagicMock):
        # Test the download coverage function
        settings = Mock()
        settings.TMP_FOLDER = 'tmp'
        
        # Create a mock project object
        project = Mock()

        # Mock the configuration attribute
        project.configuration = Mock()
        project.id = self.project_id
        
        
        mock_listObjects.return_value = self.mock_objects
        mock_copy_file_from.side_effect = self.mock_side_effects
                
        mock_get_coverage_bucket.return_value = 'test-coverage-bucket'
        
        # Create a mock project object
        project = Mock()

        # Mock the configuration attribute
        project.configuration = Mock()
        project.id = self.project_id
        
        settings = Mock()
        settings.TMP_FOLDER = 'tmp'
        settings.CACHE_PATH = 'tmp/cache'
        
        
        helper = CoverageHelper(project)
        
        # Assert that the artifacts were downloaded correctly
        assert os.listdir(f"{self.cache_folder}") == [
            'output',
            'cov_fuzzer',
            '1740399073.profraw',
            '1740399090.profraw',
            '1740399178.profraw',
            '1740399162.profraw']
        
        output_dir = f'{settings.CACHE_PATH}/coverage/{self.project_id}/'
        self.fs.create_dir(f'{settings.CACHE_PATH}/coverage/{self.project_id}/')
        helper.prepare_artifacts_package()
        
        assert "coverage.zip" in os.listdir(output_dir)
        assert os.path.getsize(f"{output_dir}/coverage.zip") > 0


