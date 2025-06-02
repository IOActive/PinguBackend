import subprocess
import os
from typing import List
from PinguApi.handlers.coverage_handlers.coverage_handler import CoverageHandler
import logging

logger = logging.getLogger(__name__)

class LLVMCoverageHandler(CoverageHandler):
    def __init__(self, profraw_files: List[str], binary_path: str, output_folder: str):
        """
        Initialize the handler with profraw files and the instrumented binary path.
        
        Args:
            profraw_files (List[str]): List of paths to .profraw files.
            binary_path (str): Path to the instrumented binary that produced the profraw files.
            output_folder (str): Folder where the coverage report will be saved.
        """
        self.profdata_file = f"coverage.profdata"  # Default output for merged data
        self.report_file = f"coverage"         # Default output for report
        self.reports = {}
        
        super().__init__(coverage_files=profraw_files, binary_path=binary_path, output_folder=output_folder)        

    def merger(self) -> bool:
        """
        Merge the .profraw files into a single .profdata file using llvm-profdata.
        
        Returns:
            bool: True if successful, False if an error occurred.
        """
        if not self.coverage_files:
            logger.warning("No .profraw files provided to merge.")
            return False
        
        # Ensure all profraw files exist
        for f in self.coverage_files:
            if not os.path.isfile(f):
                logger.error(f"Error: {f} does not exist.")
                return False
            if '.profraw' not in f:
                self.coverage_files.remove(f)
        
        # Ensure binary exists
        if not os.path.isfile(self.binary_path):
            logger.error(f"Error: Binary {self.binary_path} does not exist.")
            return False
        
        dir = os.path.dirname(self.coverage_files[0])
        self.profdata_file = f"{dir}/{self.profdata_file}"
        self.report_file = f"{dir}/{self.report_file}"

        # Construct the llvm-profdata merge command
        cmd = ["llvm-profdata", "merge", "-sparse"] + self.coverage_files + ["-o", self.profdata_file]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True, text=True)
            logger.info(f"Successfully merged {len(self.coverage_files)} .profraw files into {self.profdata_file}")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Error merging .profraw files: {e.stderr}")
            return False
        except FileNotFoundError:
            logger.error("Error: llvm-profdata not found. Ensure LLVM tools are installed and in PATH.")
            return False

    def generate_reports(self) -> bool:
        """
        Generate a coverage report from the merged .profdata file using llvm-cov.
        
        Args:
            output_format (str): Format of the report ("text" or "html"). Default: "text".
            output_file (str): Path to save the report. If None, uses self.report_file for text,
                              or "coverage_html" directory for HTML. Optional.
        
        Returns:
            bool: True if successful, False if an error occurred.
        """
        if not os.path.isfile(self.profdata_file):
            logger.error(f"Error: {self.profdata_file} not found. Run merger() first.")
            return False

        # Set default output file if not provided
        output_formats = ['json', 'lcov']

        for output_format in output_formats:
            output_file =  f"{self.output_folder}/coverage.{output_format}"
            format = f"-format={output_format}" if output_format != 'json' else ''
            # Construct the llvm-cov command
            cmd = [
                "llvm-cov", "export",
                self.binary_path,
                "-instr-profile", self.profdata_file,
                format
            ]

            try:
                with open(output_file, 'w') as output_file:
                    subprocess.run(cmd, stdout=output_file, stderr=subprocess.PIPE, text=True)
                logger.info(f"Coverage report saved to {output_file}")
                self.reports[output_format] = output_file.name
            except subprocess.CalledProcessError as e:
                logger.error(f"Error generating report: {e.stderr}")
                return False
            
        return True

    def process(self) -> bool:
        """
        Run the full process: merge .profraw files and generate a report.
        
        Args:
            output_format (str): Format of the report ("text" or "html"). Default: "text".
            output_file (str): Path to save the report. Optional.
        
        Returns:
            bool: True if both steps succeed, False otherwise.
        """
        if not self.merger():
            return False
        return self.generate_reports()
    
    def generate_final_report(self) -> str:
        """
        Return html report generated using json report and llvm-coverage-viewer tool.
        Returns:
            str: the generated report path
        """
        report_path = f"{self.output_folder}/report.html"
        
        cmd = [
            'src/resources/llvm-coverage-viewer/llvm-coverage-viewer-linux',
            '--json',
            self.reports['json'],
            '--output',
            report_path
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            logger.error(f"Error generating coverage report: {e.stderr}")
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
        
        if not os.path.exists(report_path):
            raise FileNotFoundError("Coverage report generation failed")
        
        return report_path
        