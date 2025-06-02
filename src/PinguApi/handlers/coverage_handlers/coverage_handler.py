import subprocess
import os
from typing import List


class CoverageHandler:
    def __init__(self, coverage_files: List[str], binary_path: str, output_folder: str):
        """
        Initialize the handler with raw files and the instrumented binary path.
        
        Args:
            raw_files (List[str]): List of paths to .raw files.
            binary_path (str): Path to the instrumented binary that produced the raw files.
            output_folder (str): Folder where the merged data will be stored.
        """
        self.coverage_files = coverage_files
        self.binary_path = binary_path
        self.output_folder = output_folder

    def merger(self) -> bool:
        """
        Merge the .raw files into a single .profdata file using llvm-profdata.
        
        Returns:
            bool: True if successful, False if an error occurred.
        """
        raise NotImplementedError

    def generate_reports(self) -> bool:
        """
        Generate a coverage report from the merged file.
        
        Args:
            output_format (str): Format of the report ("text" or "html" or "json"). Default: "text".
            output_file (str): Path to save the report. If None, uses self.report_file for text,
                              or "coverage_html" directory for HTML. Optional.
        
        Returns:
            bool: True if successful, False if an error occurred.
        """
        raise NotImplementedError

    def process(self) -> bool:
        """
        Run the full process: merge .raw files and generate a report.
        
        Args:
            output_format (str): Format of the report ("text" or "html" or "json"). Default: "text".
            output_file (str): Path to save the report. Optional.
        
        Returns:
            bool: True if both steps succeed, False otherwise.
        """
        raise NotImplementedError
    
    def generate_final_report(self) -> str:
        """
        Get the final merged coverage report path as a string.
        
        Returns:
            str: The merged coverage report path.
        """
        raise NotImplementedError
