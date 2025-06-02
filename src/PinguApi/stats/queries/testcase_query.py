from PinguApi.stats.queries.query import Query

class TestcaseQuery(Query):
  """The query class for TestcaseRun Query."""

  ALIAS = 't'
  
  SQL = """
  TestcaseRunStats AS (
    {query}
  )
  """

  def __init__(self, fuzz_target, query_fields, group_by, date_start,
               date_end, interval='1 day'):
        
    super().__init__(
        realted_fields=[{"name": "fuzz_target", "value": fuzz_target}],
        related_table='fuzzer_stats',
        query_fields=query_fields,
        group_by=group_by,
        date_start=date_start,
        date_end=date_end,
        table_name='fuzzer_testcase_run_stats',
        alias=TestcaseQuery.ALIAS,
        interval=interval
        )
  
  def build(self):
    """Return query."""
    query_parts = [
            'SELECT',
            self._select_fields(),
            f'FROM {self._table_name()}',
            self._join(),
            self._where(),
        ]
    
    if self._group_by():
        query_parts += [f'GROUP BY {self._group_by()}']
            
    sql = TestcaseQuery.SQL.format(
        query=(' \n'.join(query_parts))
    )

    return sql

