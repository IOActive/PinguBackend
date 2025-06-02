import os
import shutil
import zipfile
from django.conf import settings 
import yaml
from PinguApi.handlers.coverage_handlers.llvm_coverage_handler import LLVMCoverageHandler
from PinguApi.handlers.coverage_handlers.coverage_handler import CoverageHandler
import logging

from src.PinguApi.utilities import configuration
from PinguApi.submodels.project import Project
import magic
from PinguApi.handlers import storage

logger = logging.getLogger(__name__)

COVERAGE_EXTENSIONS = [
    '.cov',
    '.profraw',
    '.profdata',
    '.lcov',
    '.gcda',
    '.gcno',
    '.gcov',
    '.clover',
    '.jacoco',
    '.coverage',
    '.coverprofile',
    '.json'
]

COVERAGE_MAP = {
    LLVMCoverageHandler: ['profraw', 'profdata'],
    None: [
        'cov',
        'lcov',
        'gcda',
        'gcno',
        'gcov',
        'clover',
        'jacoco',
        'coverage',
        'coverprofile'
    ]
}

class CoverageHelper():
    def __init__(self, project:Project):
        self.project_id = str(project.id)
        self.monitored_objects = {}
        self.coverage_bucket = configuration.get_coverage_bucket(yaml.safe_load(project.configuration))
        self.cache_folders = {}
        self.flush_temporal_coverage_files()
        self.download_coverage_files()
        

    def download_coverage_files(self):
        iterator = storage.list_blobs(storage_path=f"{self.coverage_bucket}/", recursive=True)
        for obj in iterator:
            try:
                storage_file_path=f"{self.coverage_bucket}/{obj['name']}"
                response = storage.copy_file_from(storage_file_path)
                working_cache_folder = storage.cache.get_cache_folder_path(storage_file_path)
                key = storage_file_path.split("/")[1]
                if key not in self.cache_folders:
                    self.cache_folders[key] = working_cache_folder
            except Exception as e:
                print(f"Error writing file {obj['name']}: {e}")
    
    def flush_temporal_coverage_files(self):
        """
        Flushes the temporal files generate by the helper to ensure that old files are not mixed in the new executions
        """
        try:
            for key, tmp_folder in self.cache_folders.items():
                for item_name in os.listdir(tmp_folder):
                    item_path = os.path.join(tmp_folder, item_name)
                    if os.path.isfile(item_path):
                        os.remove(item_path)  # Delete file
                    elif os.path.isdir(item_path):
                        shutil.rmtree(item_path)  # Delete subdirectory
        except Exception as e:
            logging.error("Error while flushing temporal coverage files")
                
    def prepare_artifacts_package(self):
        """
        Zips all the downloaded coverage files and other artifacts into a single package for download
        """
        coverage_package_path = f'tmp/cache/coverage/{self.project_id}/coverage.zip'
        try:
            # Create a ZIP file
            for key, working_dir in self.cache_folders.items():
                with zipfile.ZipFile(coverage_package_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    coverage_files = self._get_coverage_files(working_dir)
                        
                    # Add all files in the current directory
                    for file in coverage_files:
                        file_path = os.path.realpath(file)
                        if file_path == coverage_package_path:
                            continue
                        # Write the file to the ZIP with its relative path
                        relative_path = os.path.relpath(file_path, working_dir)
                        zipf.write(file_path, relative_path)
                    
            return coverage_package_path
        except Exception as e:
            raise Exception(f"Error while creating coverage artifacts package")
                    
    def _is_executable(self, file_path):
        """
        Check if a file is an executable binary or a script.
        
        :param file_path: Path to the file.
        :return: True if the file is an executable binary or script, otherwise False.
        """
        if not os.path.isfile(file_path):
            return False
        
        # Check executable permissions
        if os.access(file_path, os.X_OK):
            return True
        
        # Check MIME type
        mime_type = magic.from_file(file_path, mime=True)
        
        # Common executable and script MIME types
        executable_mime_types = {
            "application/x-executable",  # Linux/macOS binaries
            "application/x-sharedlib",   # Shared libraries (sometimes executable)
            "application/x-msdownload",  # Windows EXE/DLL
            "application/vnd.microsoft.portable-executable",  # Windows PE format
            "application/x-mach-binary", # macOS Mach-O binaries
            "application/x-pie-executable", # Position-independent executables (PIE)
            "application/x-elf",          # ELF binaries
            "application/x-dosexec",      # DOS executables
            "application/x-object",       # Compiled object files
            "application/x-python-code",  # Compiled Python bytecode
            "text/x-python",             # Python scripts
            "text/x-shellscript",        # Shell scripts
            "text/javascript",           # JavaScript files
            "application/x-msdos-program" # MS-DOS programs
        }
        
        return mime_type in executable_mime_types
               
    def _get_binary_file(self, directory):
        # Find the binary file cotaining fuzzer in their name and checking if it is executable.
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                if 'fuzzer' in file and self._is_executable(file_path):
                    return file_path

    def _get_coverage_files(self, directory):
        """Get all coverage files in the given directory."""
        return [
            os.path.abspath(
                os.path.join(directory, f)
            ) for f in os.listdir(directory) if any(f.endswith(ext) for ext in COVERAGE_EXTENSIONS) and f != 'output']

    def _detect_coverage_handler(self, coverage_files) -> CoverageHandler:
        # by using the coverage files get the handler object
        coverage_extension = coverage_files[0].split('.')[-1]
        for handler, extensions in COVERAGE_MAP.items():
            if coverage_extension in extensions:
                return handler

    def generate_coverage_report(self):
        """Generate a coverage report for the target project."""
        result = {}
        global_coverage_files = []
        
        """
        First we generate the coverage files for each fuzzer collecting the coverage file to avoid looping twice 
        when the general project report is generated.
        """
        for key, working_directory in self.cache_folders.items():
            coverage_files = self._get_coverage_files(working_directory)
            global_coverage_files += coverage_files
            if not coverage_files:
                logger.info("No coverage files found in the specified directory.")
                return
            
            logger.info(f"Found {len(coverage_files)} coverage files to upload.")

            handler_o = self._detect_coverage_handler(coverage_files)
            
            binary_path = self._get_binary_file(working_directory)
            
            output_dir = f"{working_directory}/output"
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            if handler_o:
                handler = handler_o(coverage_files, binary_path, output_dir)
                handler.process()
                report_path = handler.generate_final_report()
                result[key] = report_path, coverage_files + [binary_path]
                    
                if not os.path.exists(report_path):
                    logger.error("Coverage report generation failed.")
                    return
            else:
                result[working_directory] = None, coverage_files + [binary_path]

        working_directory = storage.cache.get_cache_file_path(f"{self.coverage_bucket}/")
        output_dir = f"{working_directory}/output"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        handler_o = self._detect_coverage_handler(global_coverage_files)
        
        if handler_o:
            handler = handler_o(global_coverage_files, binary_path, output_dir)
            handler.process()
            report_path = handler.generate_final_report()

            if not os.path.exists(report_path):
                logger.error("Coverage report generation failed.")
                result['global'] = None, coverage_files + [binary_path]
                
            result['global'] = report_path, coverage_files + [binary_path]
            
        else:
            result['global'] = None, coverage_files + [binary_path]

        return result
                
        
    
