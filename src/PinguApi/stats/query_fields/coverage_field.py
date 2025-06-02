from src.PinguApi.stats.query_fields.base_coverage_field import BaseCoverageField
import logging
from PinguApi.stats.query_fields.common_fields import BuiltinFieldData

logger = logging.getLogger(__name__)

class CoverageField(BaseCoverageField):
  """Coverage field."""

  EDGE = 0
  FUNCTION = 1
  VALUE_TYPE = float

  def __init__(self, coverage_type, ctx=None):
    super().__init__(ctx)
    self.coverage_type = coverage_type

  def get(self, group_by, group_by_value):
    """Return data."""
    coverage_info = self.get_coverage_info(group_by, group_by_value)
    if not coverage_info:
      return None

    if self.coverage_type == self.EDGE:
      covered = coverage_info.edges_covered
      total = coverage_info.edges_total
    else:
      covered = coverage_info.functions_covered
      total = coverage_info.functions_total

    if covered is None or total is None:
      return None

    if not total:
      logger.error(
          'Invalid coverage info: total equals 0 for "%s".' % self.ctx.fuzzer)
      return BuiltinFieldData('No coverage', sort_key=0.0)

    percentage = 100.0 * float(covered) / total
    display_value = '%.2f%% (%d/%d)' % (percentage, covered, total)
    return BuiltinFieldData(display_value, sort_key=percentage)

