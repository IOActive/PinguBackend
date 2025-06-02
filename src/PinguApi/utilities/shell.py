
"""Shell related functions."""

import logging
import os
import re
import shlex
import shutil
import subprocess
import sys
import tempfile

from src.PinguBackend import environment
try:
    import psutil
except ImportError:
    psutil = None

logger = logging.getLogger(__name__)


_DEFAULT_LOW_DISK_SPACE_THRESHOLD = 5 * 1024 * 1024 * 1024  # 5 GB.
FILE_COPY_BUFFER_SIZE = 10 * 1024 * 1024  # 10 MB.
HANDLE_OUTPUT_FILE_TYPE_REGEX = re.compile(
    br'.*pid:\s*(\d+)\s*type:\s*File\s*([a-fA-F0-9]+):\s*(.*)')

_system_temp_dir = None


def _low_disk_space_threshold():
    """Get the low disk space threshold."""
    return _DEFAULT_LOW_DISK_SPACE_THRESHOLD

def sync_folders(source_folder, target_folder):
    """Synchronize two folders."""
    try:
        if not os.path.exists(target_folder):
            os.makedirs(target_folder)
            shutil.copystat(source_folder, target_folder)
            for item in os.listdir(source_folder):
                s = os.path.join(source_folder, item)
                d = os.path.join(target_folder, item)
                if os.path.isdir(s):
                    sync_folders(s, d)
                else:
                    shutil.copy(s, d)
                    shutil.copystat(s, d)
        else:
            for item in os.listdir(source_folder):
                s = os.path.join(source_folder, item)
                d = os.path.join(target_folder, item)
                if os.path.isdir(s):
                    sync_folders(s, d)
                else:
                    if not os.path.exists(d) or os.stat(s).st_mtime - os.stat(d).st_mtime > 1:
                        shutil.copy(s, d)
                        shutil.copystat(s, d)
                        print("Copied", s, "to", d)
                    else:
                        print("Skipped", s, "as it is already up to date")
        return True
    except Exception as e:
        logger.warning("Error syncing folders: {}".format(e))
        return False
                

def copy_file(source_file_path, destination_file_path):
    """Faster version of shutil.copy with buffer size."""
    if not os.path.exists(source_file_path):
        logger.error('Source file %s for copy not found.' % source_file_path)
        return False

    error_occurred = False
    try:
        with open(source_file_path, 'rb') as source_file_handle:
            with open(destination_file_path, 'wb') as destination_file_handle:
                shutil.copyfileobj(source_file_handle, destination_file_handle,
                                   FILE_COPY_BUFFER_SIZE)
    except:
        error_occurred = True

    # Make sure that the destination file actually exists.
    error_occurred |= not os.path.exists(destination_file_path)

    if error_occurred:
        logger.warning('Failed to copy source file %s to destination file %s.' %
                      (source_file_path, destination_file_path))
        return False

    return True

def create_directory(directory, create_intermediates=False, recreate=False):
    """Creates |directory|. Create intermediate directories if
  |create_intermediates|. Ignore if it already exists and |recreate| is
   False."""
    if os.path.exists(directory):
        if recreate:
            remove_directory(directory)
        else:
            return True

    try:
        if create_intermediates:
            os.makedirs(directory)
        else:
            os.mkdir(directory)
    except:
        logger.error('Unable to create directory %s.' % directory)
        return False

    return True

def execute_command(shell_command):
    """Run a command, returning its output."""
    try:
        process_handle = subprocess.Popen(
            shell_command,
            shell=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        output, _ = process_handle.communicate()
    except:
        logger.error('Error while executing command %s.' % shell_command)
        return ''

    return output


def get_command(command_line):
    """Get the command to pass to subprocess."""
    if environment.platform() == 'WINDOWS':
        return command_line

    return shlex.split(command_line, posix=True)


def get_command_line_from_argument_list(argument_list):
    """Convert a list of arguments to a string."""
    return subprocess.list2cmdline(argument_list)


def get_directory_file_count(directory_path):
    """Returns number of files within a directory (recursively)."""
    file_count = 0
    for (root, _, files) in walk(directory_path):
        for filename in files:
            file_path = os.path.join(root, filename)
            if not os.path.isfile(file_path):
                continue
            file_count += 1

    return file_count


def get_directory_size(directory_path):
    """Returns size of a directory (in bytes)."""
    directory_size = 0
    for (root, _, files) in walk(directory_path):
        for filename in files:
            file_path = os.path.join(root, filename)
            directory_size += os.path.getsize(file_path)

    return directory_size


def get_files_list(directory_path):
    """Returns a list of files in a directory (recursively)."""
    files_list = []
    for (root, _, files) in walk(directory_path):
        for filename in files:
            file_path = os.path.join(root, filename)
            if not os.path.isfile(file_path):
                continue
            files_list.append(file_path)

    return files_list


def get_free_disk_space(path='/'):
    """Return free disk space."""
    if not os.path.exists(path):
        return None

    return psutil.disk_usage(path).free


def get_interpreter(file_to_execute):
    """Gives the interpreter needed to execute |file_to_execute|."""
    interpreters = {
        '.bash': 'bash',
        '.class': 'java',
        '.js': 'node',
        '.pl': 'perl',
        '.py': sys.executable,
        '.pyc': sys.executable,
        '.sh': 'sh'
    }

    try:
        interpreter = interpreters[os.path.splitext(file_to_execute)[1]]
    except KeyError:
        return None

    return interpreter


def get_execute_command(file_to_execute):
    """Return command to execute |file_to_execute|."""
    interpreter_path = get_interpreter(file_to_execute)

    # Hack for Java scripts.
    file_to_execute = file_to_execute.replace('.class', '')

    if interpreter_path:
        command = '%s %s' % (interpreter_path, file_to_execute)
    else:
        # Handle executables that don't need an interpreter.
        command = file_to_execute
    return command


def move(src, dst):
    """Wrapper around shutil.move(src, dst). If shutil.move throws an shutil.Error
  the exception is caught, an error is logged, and False is returned."""
    try:
        shutil.move(src, dst)
        return True
    except shutil.Error:
        logger.error('Failed to move %s to %s' % (src, dst))
        return False


def remove_empty_files(root_path):
    """Removes empty files in a path recursively"""
    for directory, _, filenames in walk(root_path):
        for filename in filenames:
            path = os.path.join(directory, filename)
            if os.path.getsize(path) > 0:
                continue

            try:
                os.remove(path)
            except:
                logger.error('Unable to remove the empty file: %s (%s).' %
                               (path, sys.exc_info()[0]))


def remove_empty_directories(path):
    """Removes empty folder in a path recursively."""
    if not os.path.isdir(path):
        return

    # Remove empty sub-folders.
    files = os.listdir(path)
    for filename in files:
        absolute_path = os.path.join(path, filename)
        if os.path.isdir(absolute_path):
            remove_empty_directories(absolute_path)

    # If folder is empty, delete it.
    files = os.listdir(path)
    if not files:
        try:
            os.rmdir(path)
        except:
            logger.error('Unable to remove empty folder %s.' % path)


def remove_file(file_path):
    """Removes a file, ignoring any error if it occurs."""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except:
        pass


def remove_directory(directory, recreate=False, ignore_errors=False):
    """Removes a directory tree."""
    # Log errors as warnings if |ignore_errors| is set.
    log_error_func = logger.warning if ignore_errors else logger.error

    def clear_read_only(func, path, _):
        """Clear the read-only bit and reattempt the removal again.
    This is needed on Windows."""

        try:
            os.chmod(path, 0o750)
        except:
            # If this is tmpfs, we will probably fail.
            pass

        try:
            func(path)
        except:
            # Log errors for all cases except device or resource busy errors, as such
            # errors are expected in cases when mounts are used.
            error_message = str(sys.exc_info()[1])
            if 'Device or resource busy' not in error_message:
                logger.warning(
                    'Failed to remove directory %s failed because %s with %s failed. %s'
                    % (directory, func, path, error_message))

    # Try the os-specific deletion commands first. This helps to overcome issues
    # with unicode filename handling.
    if os.path.exists(directory):
        if environment.platform() == 'WINDOWS':
            os.system('rd /s /q "%s" > nul 2>&1' % directory)
        else:
            os.system('rm -rf "%s" > /dev/null 2>&1' % directory)

    if os.path.exists(directory):
        # 1. If directory is a mount point, then directory itself won't be
        #    removed. So, check the list of files inside it.
        # 2. If directory is a regular directory, then it should have not
        #    existed.
        if not os.path.ismount(directory) or os.listdir(directory):
            # Directory could not be cleared. Bail out.
            log_error_func('Failed to clear directory %s.' % directory)
            return False

        return True

    if not recreate:
        return True

    try:
        os.makedirs(directory)
    except:
        log_error_func('Unable to re-create directory %s.' % directory)
        return False

    return True


def walk(directory, **kwargs):
    """Wrapper around walk to resolve compatibility issues."""
    return os.walk(directory, **kwargs)
