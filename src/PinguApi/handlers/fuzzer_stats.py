
import datetime
import html
import logging
import re
from uuid import UUID

from src.PinguApi.utilities.dates_parser import parse_date
from django.utils import timezone

from PinguApi.submodels.fuzz_target import FuzzTarget
from rest_framework.exceptions import NotAcceptable, NotFound, APIException
from PinguApi.submodels.fuzzer_job_run_stats import JOB_RUN_DEFAULT_FIELDS
from PinguApi.stats.table_query import TableQuery
from PinguApi.stats.queries.group_by_query import group_by_to_field_name, parse_group_by
from django.db import connections
from PinguApi.stats.query_fields.query_field import parse_stats_column_fields, QueryField as fuzzer_stats_query_field
from PinguApi.stats.query_fields.built_in_field import BuiltinField as fuzzer_stats_builtin_field, BuiltinFieldSpecifier
import logging

logger = logging.getLogger(__name__)

class QueryField:
  """Wrapped fuzzer_stats.QueryField with extra metadata."""

  def __init__(self, field, results_index, field_type, bigquery_type):
    self.field = field
    self.results_index = results_index
    self.field_type = field_type
    self.bigquery_type = bigquery_type.lower()

class BuiltinField:
  """Wrapped fuzzer_stats.BuiltinField with extra metadata."""

  def __init__(self, spec, field):
    self.spec = spec
    self.field = field
    
def get_date(date_value, days_ago):
  """Returns |date_value| if it is not empty otherwise returns the date
    |days_ago| number of days ago."""
  if date_value:
    return date_value

  date_datetime = datetime.datetime.now(timezone.get_current_timezone()) - datetime.timedelta(days=days_ago)
  return date_datetime.strftime('%Y-%m-%d')

def _try_cast(cell, value_str, cast_function, default_value):
  """Try casting the value_str into cast_function."""
  try:
    cell["v"] = cast_function(value_str)
  except (ValueError, TypeError):
    cell["v"] = default_value
    cell["f"] = "--"

def _bigquery_type_to_charts_type(typename):
  """Convert bigquery type to charts type."""
  typename = typename.lower()
  if typename in ('integer', 'float',  'numeric', 'float8'):
    return 'number'

  if typename == 'timestamp':
    return 'date'

  return 'string'

def _python_type_to_charts_type(type_value):
  """Convert bigquery type to charts type."""
  if type_value in (int, float):
    return 'number'

  if type_value == datetime.date:
    return 'date'

  return 'string'

def _parse_stats_column_fields(results, stats_columns, group_by, fuzzer, jobs):
  """Parse stats columns.""""""
    WITH
    {job_run_subqueries}
    {}
    """
  result = []
  columns = parse_stats_column_fields(stats_columns)

  # Insert first column (group by)
  group_by_field_name = group_by_to_field_name(group_by)
  columns.insert(0, fuzzer_stats_query_field('j', group_by_field_name, None))

  contexts = {}

  for column in columns:
    if isinstance(column, fuzzer_stats_query_field):
      key = '%s_%s' % (column.table_alias, column.select_alias)

      for i, field_info in enumerate(results['fields']):
        # the 'name' field could either be "prefix_fieldname" or simply
        # "fieldname"
        if (field_info['name'] == column.select_alias or
            field_info['name'] == key):
          result.append(
              QueryField(
                field=column,
                results_index=i,
                field_type=_bigquery_type_to_charts_type(field_info['type']),
                bigquery_type=field_info['type']))
          break
    elif isinstance(column, BuiltinFieldSpecifier):
      # Builtin field.
      # Create new context if it does not exist.
      field_class = column.field_class()
      if not field_class:
        continue

      context_class = field_class.CONTEXT_CLASS
      context = contexts.setdefault(context_class, context_class(fuzzer, jobs))
      result.append(BuiltinField(column, column.create(context)))
    
  return result



def _parse_stats_column_descriptions(stats_column_descriptions):
  """Parse stats column descriptions."""
  if not stats_column_descriptions:
    return {}

  try:
    for key, value in stats_column_descriptions.items():
      stats_column_descriptions[key] = html.escape(value)

    return stats_column_descriptions
  except Exception as e:
    logger.error('Failed to parse stats column descriptions.')
    return {}

def _build_columns(result, columns):
  """Build columns."""
  for column in columns:
    if isinstance(column, QueryField):
      result["cols"].append({
          "label": column.field.select_alias,
          "type": column.field_type,
      })
    elif isinstance(column, BuiltinField):
      result['cols'].append({
          'label': column.spec.alias or column.spec.name,
          'type': _python_type_to_charts_type(column.field.VALUE_TYPE),
        }
      )


def _build_rows(result, columns, rows, group_by):
  """Build rows."""
  for row in rows:
    row_data = []
    first_column_value = None
    for column in columns:
      cell = {}
      if isinstance(column, QueryField):
        value = row[column.results_index]

        if column.field.select_alias == 'time':
          timestamp = float(value)
          time = datetime.datetime.utcfromtimestamp(timestamp)
          first_column_value = first_column_value or time
          cell["v"] = 'Date(%d, %d, %d, %d, %d, %d)' % (
              time.year, time.month - 1, time.day, time.hour, time.minute,
              time.second)
        elif column.field.select_alias == 'date':
          timestamp = float(value)
          date = datetime.datetime.utcfromtimestamp(timestamp).date()
          first_column_value = first_column_value or date
          cell["v"] = 'Date(%d, %d, %d)' % (date.year, date.month - 1, date.day)
        elif column.bigquery_type == 'integer':
          _try_cast(cell, value, int, 0)
        elif column.bigquery_type == 'float' or column.bigquery_type == 'numeric':
          # Round all float values to single digits.
          _try_cast(cell, value, lambda s: round(float(s), 1), 0.0)
        else:
          cell["v"] = value

        first_column_value = first_column_value or cell["v"]
            
      elif isinstance(column, BuiltinField):
        data = column.field.get(group_by, first_column_value)
        if data:
          formatted_value = data.value
          """ if data.link:
            link = (
                _get_cloud_storage_link(data.link)
                if data.link.startswith('https://') else data.link)
            formatted_value = '<a href="%s">%s</a>' % (link, data.value) """

          if data.sort_key is not None:
            cell["v"] = data.sort_key
          else:
            cell["v"] = data.value

          if data.sort_key is not None or data.link:
            cell["f"] = formatted_value
        else:
          cell["v"] = ''
          cell["f"] = '--'
      
      row_data.append(cell) 
    result["rows"].append({"c": row_data})

def _do_bigquery_query(query):
  """Return results from BigQuery."""
  logger.info(query)
  try:
    with connections['bigquery'].cursor() as cursor:
        cursor.execute(query)
        # Map the type codes to human-readable types (using psycopg2.extensions)
        type_map = {
            23: "integer",
            20: "integer",
            1043: "varchar",
            1700: "numeric",
            701: "float8",
            1082: "date",
            1114: "timestamp",
            # Add more type codes as necessary
        }
        
        results = {
          "fields": [],
          'rows': []
        }
        
        for desc in cursor.description:
            field = {}
            field['name'] = desc[0]
            field['type'] = type_map.get(desc[1], "unknown")
            results["fields"].append(field)
        
        # Fetch results and map to column names
        
        for row in cursor.fetchall():
            # Map the row data to column names and store it as a dictionary
            results['rows'].append(row)

        return results

  except Exception as e:
    logger.info(query)
    raise Exception

def parse_interval(interval):
  # PostgreSQL time interval for how long each bucket is
  # Ensure that interval following the expected nomenclature of '30 days', '2 hours' etc with a regex expresion
  if re.match(r'^\d+ (seconds|second|minutes|minute|hours|hour|days|day|weeks|week|months|month|year|years)$', interval):
    return interval
  else:
    raise ValueError("Invalid interval format")
  
def clean_malformed_result(result):
  # Clean up row with malformed data, not sure why sometime we get a row all -- f, -- f values are None
  for row in result['rows']:
    malformed_count = 0
    for value in row["c"]:
      # Is malformed if all the entries are None or '-- f'
      if (value['v'] in ['', '--'] or value['v'] == 0) or 'f' in value or value['v'] == None:
        malformed_count += 1
    if malformed_count == len(row["c"]):
      # Remove the row if it's malformed
      result['rows'].remove(row)
  return result

def build_results(fuzz_target_id: UUID, group_by, start_date, end_date, interval='1 day'):
  """Build results."""
  date_start = parse_date(start_date)
  date_end = parse_date(end_date)
  interval = parse_interval(interval)
  
  try:
      fuzztarget = FuzzTarget.objects.get(id=fuzz_target_id)
  except Exception as e:
      raise NotFound(detail='Fuzz target not found', code=404)
  
  if fuzztarget.fuzzer.stats_columns:
    stats_columns = fuzztarget.fuzzer.stats_columns
  else:
    stats_columns = JOB_RUN_DEFAULT_FIELDS
    
  group_by = parse_group_by(group_by)
  
  if group_by is None:
    raise NotAcceptable(detail="Invalid grouping.", code=406)
  
  try:
    table_query = TableQuery(str(fuzztarget.id), stats_columns, group_by, date_start, date_end, interval)
    results = _do_bigquery_query(table_query.build())
  
    result = {
        "cols": [],
        "rows": [],
        "column_descriptions":
            _parse_stats_column_descriptions(
                fuzztarget.fuzzer.stats_column_descriptions),
    }
    
    fuzzer_name = f"{fuzztarget.fuzzer.name}_{fuzztarget.binary}"
    try:
      columns = _parse_stats_column_fields(results, stats_columns, group_by, fuzztarget.fuzzer.id, None)
    except Exception as e:
      raise APIException(detail="", code=500)
    _build_columns(result, columns)
    _build_rows(result, columns, results['rows'], group_by)

    result = clean_malformed_result(result)
    return result
  
  except Exception as e:
    raise Exception