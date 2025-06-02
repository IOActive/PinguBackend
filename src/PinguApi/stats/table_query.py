from PinguApi.stats.query_fields.query_field import QueryField, parse_stats_column_fields
from PinguApi.stats.queries.job_query import JobQuery
from PinguApi.stats.queries.group_by_query import QueryGroupBy, group_by_to_field_name
from PinguApi.stats.queries.testcase_query import TestcaseQuery
      
        
class TableQuery:
  """Query for generating results in a table."""

  def __init__(self, fuzz_target, stats_columns, group_by,
               date_start, date_end, interval):
    assert group_by

    self.fuzz_target = fuzz_target
    self.group_by = group_by
    self.date_start = date_start
    self.date_end = date_end
    self.job_run_query = None
    self.testcase_run_query = None
    self.interval = interval

    self.job_run_fields = []
    self.testcase_run_fields = []
    fields = parse_stats_column_fields(stats_columns)

    for field in fields:
      # Split up fields by table.
      if not isinstance(field, QueryField):
        continue

      if field.table_alias == JobQuery.ALIAS:
        self.job_run_fields.append(field)
      elif field.table_alias == TestcaseQuery.ALIAS:
        self.testcase_run_fields.append(field)
    
    self.table_columns = []
    for field in self.testcase_run_fields + self.job_run_fields:
      self.table_columns.append(field.select_alias)

    #  subqueries.

    # For query by time, we can't correlate the time of testcase run with a job
    # run since they are set at different times. So, use only the results from
    # testcase run and don't join them with job run, see build(). Also, the job
    # parameters like: known crashes, new crashes are aggregate numbers from job
    # that are not applicable to show per testcase run (a point on graph).
    if self.job_run_fields and self.group_by != QueryGroupBy.GROUP_BY_TIME:
      self.job_run_query = JobQuery(fuzz_target=fuzz_target,
                                    query_fields=self.job_run_fields,
                                    group_by=group_by, 
                                    date_start=date_start,
                                    date_end=date_end,
                                    interval=self.interval)
    if self.testcase_run_fields:
      self.testcase_run_query = TestcaseQuery(fuzz_target,
                                              self.testcase_run_fields, group_by,
                                              date_start, date_end, self.interval)
    
    assert self.job_run_query or self.testcase_run_query, ('Unable to create query.')
  
  
  def _format_field_list(self, fields, prefix, force=False):
    # If only one field, return it without comma
    
    if len(fields) == 1 and force:
      return f"{prefix}.{fields[0].select_alias},"
    
    elif len(fields) == 1:
        return f"{prefix}.{fields[0].select_alias}"
    
    # For multiple fields, join with a comma and newline but omit the trailing comma
    return ", \n".join([f"{prefix}.{field.select_alias}" for field in fields])
  
  def _join_subqueries(self):
    """Create an inner join for subqueries."""
    group_by = group_by_to_field_name(self.group_by)
    if group_by:
      SQL = """
      WITH
        {job_subquery}
        {testcase_subquery}
        SELECT
        {job_fileds}
        {testcase_fileds}
        FROM JobRunWithSummary jrs
        LEFT JOIN TestcaseRunStats tcrs ON jrs.{group_by} = tcrs.{group_by} AND jrs.interval = tcrs.interval;
      """
      join_query = SQL.format(
        job_subquery=self.job_run_query.build(),
        testcase_subquery=self.testcase_run_query.build(),
        group_by=group_by_to_field_name(self.group_by),
        testcase_fileds=self._format_field_list(self.testcase_run_fields, "tcrs"),
        job_fileds=self._format_field_list(self.job_run_fields, "jrs", force=True),
      )
    else:
      SQL = """
      WITH
        {job_subquery}
        {testcase_subquery}
        SELECT
        {job_fileds}
        {testcase_fileds}
        FROM JobRunWithSummary jrs
        LEFT JOIN TestcaseRunStats tcrs ON jrs.interval = tcrs.interval;
      """
      join_query = SQL.format(
        job_subquery=self.job_run_query.build(),
        testcase_subquery=self.testcase_run_query.build(),
        testcase_fileds=self._format_field_list(self.testcase_run_fields, "tcrs"),
        job_fileds=self._format_field_list(self.job_run_fields, "jrs", force=True),
      )
    return join_query

  def _single_subquery(self, query, query_fields, table_reference):
    """Create a single subquery."""
    SQL = """
    WITH
      {query}
      SELECT
      {query_fields}
      FROM {table_reference}
    """
    return SQL.format(
      query=query,
      query_fields=query_fields,
      table_reference=table_reference
    )
  
  def build(self):
    """Build the table query."""   
    if self.job_run_query and self.testcase_run_query:
      return self._join_subqueries()
    elif self.job_run_query:
      return self._single_subquery(
        query=self.job_run_query.build(),
        query_fields=self._format_field_list(self.job_run_fields, "jrs", force=True),
        table_reference='JobRunWithSummary jrs')
    elif self.testcase_run_query:
      return self._single_subquery(
        query=self.testcase_run_query.build(),
        query_fields=self._format_field_list(self.testcase_run_fields, "tcrs", force=True),
        table_reference='TestcaseRunStats tcrs'
        )
    else:
      raise ValueError("No query provided")
