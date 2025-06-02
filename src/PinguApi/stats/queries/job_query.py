from typing import List

from PinguApi.stats.query_fields.query_field import QueryField
from PinguApi.stats.queries.query import Query


class JobQuery(Query):
  """The query class for JobRun Query."""

  DEFAULT_FIELDS = """
    sum(j.testcases_executed) as testcases_executed,
    custom(j.total_crashes) as total_crashes,
    custom(j.new_crashes) as new_crashes,
    custom(j.known_crashes) as known_crashes
  """
  SQL = """
  JobRunWithConcatedCrashes AS (
    SELECT
      {select_fields},
      ARRAY_AGG(crashes) AS crashes
    FROM
      {table_name}
    {join}
    {where}
    GROUP BY
      {group_by}
  ),
  jobRunWithUniqueCrashes AS (
    SELECT
      {select_fields_aliases}
      interval,
      ARRAY(
        SELECT ROW(
          (crash_data->>'crash_type')::text,
          (crash_data->>'security_flag')::boolean,
          SUM((crash_data->>'count')::float)::int,  -- Explicitly cast the sum to int
          MAX(CASE WHEN (crash_data->>'is_new')::boolean THEN 1 ELSE 0 END)  
        )
        FROM
        JobRunWithConcatedCrashes,
        LATERAL unnest(crashes) AS crash, -- Unnest the crashes array
        LATERAL jsonb_array_elements(crash->'crashes') AS crash_data -- Unnest the inner crashes array
        GROUP BY crash_data->>'crash_type', crash_data->>'security_flag', crash_data->>'crash_state'
      ) AS crashes
    FROM
      JobRunWithConcatedCrashes
  ),
  JobRunWithSummary AS (
    SELECT
      interval,
      {select_fields_aliases}
      -- Unpacking the crash_count ROW structure into individual fields
      COALESCE(SUM(cd.count)::float, 0) AS total_crashes,
      COUNT(CASE WHEN cd.is_new = 1 THEN 1 END) AS new_crashes_count,
      COUNT(CASE WHEN cd.is_new = 0 THEN 1 END) AS known_crashes_count,
      COUNT(cd) as unique_crashes
    FROM
      JobRunWithUniqueCrashes,
      LATERAL (
        SELECT
          (crash_data).count,
          (crash_data).is_new
        FROM UNNEST(crashes) AS crash_data(
          crash_type text, 
          security_flag boolean, 
          count int, 
          is_new int
        )
      ) AS cd
    GROUP BY
      {select_fields_aliases} interval
  ),
"""
  ALIAS = 'j'

  def __init__(self, fuzz_target, query_fields: List[QueryField], group_by, date_start,
               date_end, interval='1 day'):

    super().__init__(
        realted_fields=[{"name": "fuzz_target", "value": fuzz_target}],
        related_table='fuzzer_stats',
        query_fields=query_fields,
        group_by=group_by,
        date_start=date_start,
        date_end=date_end,
        table_name='fuzzer_job_run_stats',
        alias=JobQuery.ALIAS,
        interval=interval
        )

  def build(self):
    """Return query."""
    sql = JobQuery.SQL.format(
        table_name=self._table_name(),
        select_fields=self._select_fields(),
        group_by=self._group_by(),
        where=self._where(),
        join=self._join(),
        select_fields_aliases=self._format_field_list(self.query_fields) 
    )

    return sql