
import re
from datetime import datetime
from django.utils import timezone

def parse_date(date_str):
  """Parse YYYY-MM-DD."""
  if not date_str:
    return None

  dt = datetime.strptime(date_str, "%Y-%m-%d")
  return dt.replace(tzinfo=timezone.get_current_timezone())  # Make it timezone-aware (Django default).