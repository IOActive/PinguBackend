class QueryGroupBy:
  """GroupBy enum."""
  GROUP_BY_NONE = 0
  GROUP_BY_REVISION = 1
  GROUP_BY_INTERVAL = 2
  GROUP_BY_TIME = 3
  GROUP_BY_JOB = 4
  GROUP_BY_FUZZ_TARGET = 5
  
  
def parse_group_by(group_by):
  """Parse group_by value."""
  if group_by == 'by-interval':
    return QueryGroupBy.GROUP_BY_INTERVAL
  if group_by == 'by-time':
    return QueryGroupBy.GROUP_BY_TIME
  if group_by == 'by-revision':
    return QueryGroupBy.GROUP_BY_REVISION
  if group_by == 'by-job':
    return QueryGroupBy.GROUP_BY_JOB
  if group_by == 'by-fuzztarget':
    return QueryGroupBy.GROUP_BY_FUZZ_TARGET
  if group_by == QueryGroupBy.GROUP_BY_TIME:
    return 'time'

  return None

def group_by_to_field_name(group_by):
  """Convert QueryGroupBy value to its corresponding field name."""
  if group_by == QueryGroupBy.GROUP_BY_REVISION:
    return 'build_revision'
  
  if group_by == QueryGroupBy.GROUP_BY_JOB:
    return 'job'

  if group_by == QueryGroupBy.GROUP_BY_FUZZ_TARGET:
    return 'fuzz_target'
  
  if group_by == QueryGroupBy.GROUP_BY_TIME:
    return 'time'
  
  return None