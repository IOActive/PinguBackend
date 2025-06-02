import datetime
import re
from PinguApi.subtests.views.pingu_api_testcase import PinguAPITestCase
from PinguApi.stats.query_fields.query_field import QueryField, parse_stats_column_fields
from PinguApi.stats.queries.group_by_query import QueryGroupBy
from PinguApi.stats.queries.job_query import JobQuery
from PinguApi.stats.query_fields.built_in_field import BuiltinFieldSpecifier
from PinguApi.stats.query_fields.coverage_field import CoverageField
from PinguApi.stats.table_query import TableQuery


def sanitize_sql(s):
  """Sanitize the sql by removing all new lines and surrounding whitespace."""
  s = re.sub('[ \\s\n\r]*\n[ \\s\n\r]*', ' ', s, flags=re.MULTILINE)
  s = re.sub('\\([ \t]+', '(', s)
  s = re.sub('[ \t]+\\)', ')', s)
  return s.strip()

class BigQueryStatsTests(PinguAPITestCase):
  """BigQuery stats tests."""

  def setUp(self):
    super().setUp()

  def test_parse_stats_column_fields(self):
    """Tests stats column parsing."""
    fields = parse_stats_column_fields(
        'sum(t.abc), avg(j.abc) as bcd, custom(j.def) as def,  '
        '_EDGE_COV, _FUNC_COV as 123,\n'
        '_COV_REPORT as blahblah, _CORPUS_SIZE as corpus_size, '
        '_CORPUS_BACKUP as corpus_backup')

    self.assertEqual(len(fields), 8)

    self.assertIsInstance(fields[0], QueryField)
    self.assertEqual(fields[0].aggregate_function, 'sum')
    self.assertFalse(fields[0].is_custom())
    self.assertEqual(fields[0].name, 'abc')
    self.assertEqual(fields[0].table_alias, 't')
    # select_alias is defauled to name.
    self.assertEqual(fields[0].select_alias, 'abc')

    self.assertIsInstance(fields[1], QueryField)
    self.assertEqual(fields[1].aggregate_function, 'avg')
    self.assertFalse(fields[1].is_custom())
    self.assertEqual(fields[1].name, 'abc')
    self.assertEqual(fields[1].table_alias, 'j')
    self.assertEqual(fields[1].select_alias, 'bcd')

    self.assertIsInstance(fields[2], QueryField)
    self.assertEqual(fields[2].aggregate_function, 'custom')
    self.assertTrue(fields[2].is_custom())
    self.assertEqual(fields[2].name, 'def')
    self.assertEqual(fields[2].table_alias, 'j')
    self.assertEqual(fields[2].select_alias, 'def')

    self.assertIsInstance(fields[3], BuiltinFieldSpecifier)
    self.assertEqual(fields[3].name, '_EDGE_COV')
    self.assertEqual(fields[3].field_class(), CoverageField)
    self.assertIsNone(fields[3].alias)

    self.assertIsInstance(fields[4], BuiltinFieldSpecifier)
    self.assertEqual(fields[4].name, '_FUNC_COV')
    self.assertEqual(fields[4].field_class(), CoverageField)
    self.assertEqual(fields[4].alias, '123')

    """     
    self.assertIsInstance(fields[5], BuiltinFieldSpecifier)
    self.assertEqual(fields[5].name, '_COV_REPORT')
    self.assertEqual(fields[5].field_class(), CoverageReportField)
    self.assertEqual(fields[5].alias, 'blahblah')

    self.assertIsInstance(fields[6], BuiltinFieldSpecifier)
    self.assertEqual(fields[6].name, '_CORPUS_SIZE')
    self.assertEqual(fields[6].field_class(), CorpusSizeField)
    self.assertEqual(fields[6].alias, 'corpus_size')

    self.assertIsInstance(fields[7], BuiltinFieldSpecifier)
    self.assertEqual(fields[7].name, '_CORPUS_BACKUP')
    self.assertEqual(fields[7].field_class(), CorpusBackupField)
    self.assertEqual(fields[7].alias, 'corpus_backup')
    """

    # Test that invalid fields are ignored.
    fields = parse_stats_column_fields(
        'sum(abc)  ,   min(t.bcd)    as bcd   , '
        'sum(t.def) as "1, _EDGE_COV as ""1"')
    self.assertEqual(len(fields), 1)
    self.assertIsInstance(fields[0], QueryField)
    self.assertEqual(fields[0].aggregate_function, 'min')
    self.assertEqual(fields[0].name, 'bcd')
    self.assertEqual(fields[0].table_alias, 't')
    self.assertEqual(fields[0].select_alias, 'bcd')

  def test_query_job_day(self):
    """Tests querying for JobRuns grouped by day."""
    fields = parse_stats_column_fields(
        JobQuery.DEFAULT_FIELDS)
    query = JobQuery('fuzzer_name',
                    fields,
                    QueryGroupBy.GROUP_BY_TIME,
                    datetime.date(2016, 10, 1),
                    datetime.date(2016, 10, 7))
    excepted_result = f"""
    JobRunWithConcatedCrashes AS (
      SELECT
        time, 
      sum(j.testcases_executed) as testcases_executed, 
      custom(j.total_crashes) as total_crashes, 
      custom(j.new_crashes) as new_crashes, 
      custom(j.known_crashes) as known_crashes, 
      time_bucket('1 day', j.time) as interval,
            ARRAY_AGG(crashes) AS crashes
          FROM
            fuzzer_job_run_stats j
          INNER JOIN fuzzer_stats ON j.fuzzer_stats_id = fuzzer_stats.id
          WHERE  fuzzer_stats.fuzz_target = 'fuzzer_name'
      AND j.time > '2016-10-01'::timestamptz
      AND j.time < '2016-10-07'::timestamptz

          GROUP BY
            j.time, interval
        ),
        jobRunWithUniqueCrashes AS (
          SELECT
            testcases_executedtime, 
      total_crashestime, 
      new_crashestime, 
      known_crashes
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
            testcases_executedtime, 
      total_crashestime, 
      new_crashestime, 
      known_crashes
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
            testcases_executedtime, 
      total_crashestime, 
      new_crashestime, 
      known_crashes interval
        ),
"""
    self.assertEqual(
        sanitize_sql(query.build()),
        sanitize_sql(excepted_result))

  def test_query_job_revision(self):
    """Tests querying for JobRuns grouped by revision."""
    fields = parse_stats_column_fields(
        JobQuery.DEFAULT_FIELDS)
    query = JobQuery('fuzzer_name',
                    fields,
                    QueryGroupBy.GROUP_BY_REVISION,
                    datetime.date(2016, 10, 1),
                    datetime.date(2016, 10, 7))
    expected_result = """
    JobRunWithConcatedCrashes AS (
    SELECT
      fuzzer_stats.build_revision, 
      sum(j.testcases_executed) as testcases_executed, 
      custom(j.total_crashes) as total_crashes, 
      custom(j.new_crashes) as new_crashes, 
      custom(j.known_crashes) as known_crashes, 
      time_bucket('1 day', j.time) as interval,
            ARRAY_AGG(crashes) AS crashes
          FROM
            fuzzer_job_run_stats j
          INNER JOIN fuzzer_stats ON j.fuzzer_stats_id = fuzzer_stats.id
          WHERE  fuzzer_stats.fuzz_target = 'fuzzer_name'
      AND j.time > '2016-10-01'::timestamptz
      AND j.time < '2016-10-07'::timestamptz

          GROUP BY
            fuzzer_stats.build_revision, interval
        ),
        jobRunWithUniqueCrashes AS (
          SELECT
            testcases_executedbuild_revision, 
      total_crashesbuild_revision, 
      new_crashesbuild_revision, 
      known_crashes
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
            testcases_executedbuild_revision, 
      total_crashesbuild_revision, 
      new_crashesbuild_revision, 
      known_crashes
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
            testcases_executedbuild_revision, 
      total_crashesbuild_revision, 
      new_crashesbuild_revision, 
      known_crashes interval
        ),
          
    """
    self.assertEqual(
        sanitize_sql(query.build()),
        sanitize_sql(expected_result))

  def test_query_job_fuzzer_fuzztarget(self):
    """Tests querying for JobRuns grouped by fuzzer."""
    fields = parse_stats_column_fields(
        JobQuery.DEFAULT_FIELDS)
    query = JobQuery('fuzzer_name',
                    fields,
                    QueryGroupBy.GROUP_BY_FUZZ_TARGET,
                    datetime.date(2016, 10, 1),
                    datetime.date(2016, 10, 7))
    expected_result = """
      JobRunWithConcatedCrashes AS (
    SELECT
      fuzzer_stats.fuzz_target, 
      sum(j.testcases_executed) as testcases_executed, 
      custom(j.total_crashes) as total_crashes, 
      custom(j.new_crashes) as new_crashes, 
      custom(j.known_crashes) as known_crashes, 
      time_bucket('1 day', j.time) as interval,
            ARRAY_AGG(crashes) AS crashes
          FROM
            fuzzer_job_run_stats j
          INNER JOIN fuzzer_stats ON j.fuzzer_stats_id = fuzzer_stats.id
          WHERE  fuzzer_stats.fuzz_target = 'fuzzer_name'
      AND j.time > '2016-10-01'::timestamptz
      AND j.time < '2016-10-07'::timestamptz

          GROUP BY
            fuzzer_stats.fuzz_target, interval
        ),
        jobRunWithUniqueCrashes AS (
          SELECT
            testcases_executedfuzz_target, 
      total_crashesfuzz_target, 
      new_crashesfuzz_target, 
      known_crashes
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
            testcases_executedfuzz_target, 
      total_crashesfuzz_target, 
      new_crashesfuzz_target, 
      known_crashes
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
            testcases_executedfuzz_target, 
      total_crashesfuzz_target, 
      new_crashesfuzz_target, 
      known_crashes interval
        ),
          
    """
    self.assertEqual(
        sanitize_sql(query.build()),
        sanitize_sql(expected_result))

  def test_table_query_join(self):
    """Tests basic table query involving a join."""
    stats_columns = """
      sum(j.testcases_executed) as testcases_executed,
      custom(j.total_crashes) as total_crashes,
      custom(j.new_crashes) as new_crashes,
      custom(j.known_crashes) as known_crashes,
      avg(t.average_exec_per_sec) as average_exec_per_sec
    """

    query = TableQuery('fuzzer_name',
                      stats_columns,
                      QueryGroupBy.GROUP_BY_TIME,
                      datetime.date(2016, 10, 1),
                      datetime.date(2016, 10, 7),
                      interval='1 day')
    
    expected_result = """
       WITH
      
      TestcaseRunStats AS (
        SELECT 
          time, 
          avg((t.custom_stats->>'average_exec_per_sec')::float) as average_exec_per_sec, 
          time_bucket('1 day', t.time) as interval 
          FROM fuzzer_testcase_run_stats t 
          INNER JOIN fuzzer_stats ON t.fuzzer_stats_id = fuzzer_stats.id 
          WHERE  fuzzer_stats.fuzz_target = 'fuzzer_name'
          AND t.time > '2016-10-01'::timestamptz
          AND t.time < '2016-10-07'::timestamptz
      
        GROUP BY t.time, interval
          )
        
      SELECT
        tcrs.average_exec_per_sec,
      FROM TestcaseRunStats tcrs
    
    """
    self.assertEqual(
        sanitize_sql(query.build()),
        sanitize_sql(expected_result))

  def test_table_query_single(self):
    """Tests basic table query involving single subquery."""
    stats_columns = """
      sum(j.testcases_executed) as testcases_executed,
      custom(j.total_crashes) as total_crashes,
      custom(j.new_crashes) as new_crashes,
      custom(j.known_crashes) as known_crashes
    """

    query = TableQuery('fuzzer_name',
                      stats_columns,
                      QueryGroupBy.GROUP_BY_FUZZ_TARGET,
                      datetime.date(2016, 10, 1),
                      datetime.date(2016, 10, 7),
                      interval='1 day')
    

    expected_result = """
    
    WITH
    JobRunWithConcatedCrashes AS (
      SELECT
        fuzzer_stats.fuzz_target, 
  sum(j.testcases_executed) as testcases_executed, 
  custom(j.total_crashes) as total_crashes, 
  custom(j.new_crashes) as new_crashes, 
  custom(j.known_crashes) as known_crashes, 
  time_bucket('1 day', j.time) as interval,
        ARRAY_AGG(crashes) AS crashes
      FROM
        fuzzer_job_run_stats j
      INNER JOIN fuzzer_stats ON j.fuzzer_stats_id = fuzzer_stats.id
      WHERE  fuzzer_stats.fuzz_target = 'fuzzer_name'
  AND j.time > '2016-10-01'::timestamptz
  AND j.time < '2016-10-07'::timestamptz

      GROUP BY
        fuzzer_stats.fuzz_target, interval
    ),
    jobRunWithUniqueCrashes AS (
      SELECT
        testcases_executedfuzz_target, 
  total_crashesfuzz_target, 
  new_crashesfuzz_target, 
  known_crashes
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
        testcases_executedfuzz_target, 
  total_crashesfuzz_target, 
  new_crashesfuzz_target, 
  known_crashes
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
        testcases_executedfuzz_target, 
  total_crashesfuzz_target, 
  new_crashesfuzz_target, 
  known_crashes interval
    ),

        SELECT
        jrs.testcases_executed, 
  jrs.total_crashes, 
  jrs.new_crashes, 
  jrs.known_crashes
        FROM JobRunWithSummary jrs
    """
    self.assertEqual(
        sanitize_sql(query.build()),
        sanitize_sql(expected_result))