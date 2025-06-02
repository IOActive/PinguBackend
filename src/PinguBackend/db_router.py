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

import logging
from PinguApi.models import bigquery_models

logger = logging.getLogger(__name__)

class DatabaseRouter:
    def db_for_read(self, model, **hints):
        """Point read operations to the appropriate database."""
        if model._meta.app_label == 'PinguApi':
            if model._meta.model_name.lower() in bigquery_models:
                return 'bigquery'
            return 'primary'
        return 'default'

    def db_for_write(self, model, **hints):
        """Point write operations to the appropriate database."""
        if model._meta.app_label == 'PinguApi':
            if model._meta.model_name.lower() in bigquery_models:
                return 'bigquery'
            return 'primary'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        """Allow any relation if both models are in the same database."""
        db_list = ('default', 'primary', 'bigquery')
        if obj1._state.db in db_list and obj2._state.db in db_list:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """Ensure that only models for a database get created in that database."""     
        if app_label == 'PinguApi':
            if model_name.lower() in bigquery_models:
                return db == 'bigquery'
            return db == 'primary'
        return db == 'default'



