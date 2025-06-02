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

# ENVIRONMENT = 'local'
import sys


ENVIRONMENT = 'development'
# ENVIRONMENT = 'production'

SETTINGS_MODULE = 'PinguBackend.settings.development'

if ENVIRONMENT == 'docker_dev':
    SETTINGS_MODULE = 'PinguBackend.settings.docker_dev'
if ENVIRONMENT == 'docker_prod':
    SETTINGS_MODULE = 'PinguBackend.settings.docker_prod'
if ENVIRONMENT == 'development':
    SETTINGS_MODULE = 'PinguBackend.settings.development'
if ENVIRONMENT == 'production':
    SETTINGS_MODULE = 'PinguBackend.settings.production'

def platform():
    """Return the operating system type, unless an override is provided."""

    if sys.platform.startswith('win'):
        return 'WINDOWS'
    if sys.platform.startswith('linux'):
        return 'LINUX'
    if sys.platform == 'darwin':
        return 'MAC'

    raise ValueError('Unsupported platform "%s".' % sys.platform)