from PinguApi.submodels.coverage import Coverage
from PinguApi.stats.queries.group_by_query import QueryGroupBy
from PinguApi.stats.query_fields.builtin_field_context import BuiltinFieldContext

class CoverageFieldContext(BuiltinFieldContext):
  """Coverage field context. Acts as a cache."""

  def __init__(self, fuzzer=None, jobs=None):
    super().__init__(fuzzer=fuzzer, jobs=jobs)

  def get_coverage_info(self, fuzzer, date=None) -> Coverage:
    """Return coverage info of child fuzzers."""
    try:
      query = Coverage.objects.all()  # Get base queryset
      query = query.filter(fuzzer=fuzzer)  # Apply filter
        
      if date:
        query = query.filter(data=date)  # Apply date filter if provided
        
      return query
    except Exception as e:
      raise Exception(f"Error getting coverage info")
  

class BaseCoverageField:
  """Base builtin field class for coverage related fields."""

  CONTEXT_CLASS = CoverageFieldContext

  def __init__(self, ctx:CONTEXT_CLASS):
    self.ctx = ctx

  def get_coverage_info(self, group_by, group_by_value):
    """Return coverage information."""
    coverage_info = None
    if group_by == QueryGroupBy.GROUP_BY_INTERVAL:
      # Return coverage data for the fuzzer and the day.
      coverage_info = self.ctx.get_coverage_info(self.ctx.fuzzer)

    elif group_by == QueryGroupBy.GROUP_BY_FUZZ_TARGET:
      # Return latest coverage data for each fuzzer.
      coverage_info = self.ctx.get_coverage_info(self.ctx.fuzzer)

    elif group_by == QueryGroupBy.GROUP_BY_JOB:
      # Return the latest coverage data for the fuzzer. Even though we group by
      # job here, coverage information does not differ across jobs. As of now,
      # it only depends on the fuzzer name and the date.
      coverage_info = self.ctx.get_coverage_info(self.ctx.fuzzer)

    return coverage_info
