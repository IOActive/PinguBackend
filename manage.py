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

#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from django.conf import settings 
from src.scripts.load_config_to_env import load_config_env
from src.PinguBackend.environment import SETTINGS_MODULE

def main():
    """Run administrative tasks."""
    
    # load backend component configuration into enviroment context
    load_config_env("config/system/config.yaml")
    load_config_env("config/redis/config.yaml")
    load_config_env("config/database/config.yaml")
    load_config_env("config/minio/config.yaml")
    
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", SETTINGS_MODULE)
    sys.path.insert(0, os.path.abspath(os.path.join('src')))
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
