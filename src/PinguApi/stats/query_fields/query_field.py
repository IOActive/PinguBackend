import re

from PinguApi.stats.query_fields.built_in_field import BuiltinFieldSpecifier
from src.PinguApi.stats.queries.testcase_query import TestcaseQuery

def parse_stats_column_fields(column_fields):
  """Parse the stats column fields."""
  # e.g. 'sum(t.field_name) as display_name'.
  aggregate_regex = re.compile(r'^(\w+)\(([a-z])\.([^\)]+)\)(\s*as\s*(\w+))?$')

  # e.g. '_EDGE_COV as blah'.
  builtin_regex = re.compile(r'^(_\w+)(\s*as\s*(\w+))?$')
  
  # Matches aggregate functions with arithmetic operations inside the parentheses (e.g., sum(t.field_name*100))
  aggregate_with_arithmetic_regex = re.compile(r'^(\w+)\(([a-z])\.([^\+\-\*/\(\)\d]+)([\+\-\*/\(\)\d]+.*)\)(\s*as\s*(\w+))?$')


  fields = []
  parts = [field.strip() for field in column_fields.split(',')]
  for part in parts:
    
    # Handle aggregate expressions with arithmetic operations (e.g., sum(t.field_name*100))
    match = aggregate_with_arithmetic_regex.match(part)
    if match:
        table_alias = match.group(2)
        field_name = match.group(3)
        aggregate_function = match.group(1)
        arithmetic_expression = match.group(4)  # Capture the full arithmetic expression
        select_alias = match.group(6)
        if select_alias:
            select_alias = select_alias.strip('"')

        # Create QueryField with arithmetic expression
        fields.append(QueryField(table_alias=table_alias, field_name=field_name, aggregate_function=aggregate_function, arithmetic_operant=arithmetic_expression, select_alias=select_alias, ))
        continue
          
    match = aggregate_regex.match(part)
    if match:
      table_alias = match.group(2)
      field_name = match.group(3)
      aggregate_function = match.group(1)
      select_alias = match.group(5)
      if select_alias:
        select_alias = select_alias.strip('"')

      fields.append(QueryField(table_alias=table_alias, field_name=field_name, aggregate_function=aggregate_function, select_alias=select_alias))
      continue

    match = builtin_regex.match(part)
    if match:
      name = match.group(1)
      alias = match.group(3)
      if alias:
        alias = alias.strip('"')
      fields.append(BuiltinFieldSpecifier(name, alias))
      continue

  return fields

class QueryField:
  """Represents a query field."""

  def __init__(self,
               table_alias,
               field_name,
               aggregate_function,
               arithmetic_operant = None,
               select_alias=None):
    
    self.table_alias = table_alias
    self.name = field_name
    self.aggregate_function = aggregate_function
    self.arithmetic_operant = arithmetic_operant
    self.select_alias = select_alias or field_name

  def is_custom(self):
    """Return true if this field uses complex query. This field won't appear
      in the SELECT's fields automatically. We will need to define how to get
      the data."""
    return (self.aggregate_function and
            self.aggregate_function.lower() == 'custom')

  def __str__(self):
    if self.table_alias == TestcaseQuery.ALIAS:
      if self.aggregate_function and self.arithmetic_operant:
        result = f"{self.aggregate_function}(({self.table_alias}.custom_stats->>'{self.name}')::float){self.arithmetic_operant}"
      elif self.aggregate_function:
        result = f"{self.aggregate_function}(({self.table_alias}.custom_stats->>'{self.name}')::float)"
      else:
        result = f"{self.table_alias}.custom_stats->>'{self.name}'"
    else:
      if self.aggregate_function:
        result = f'{self.aggregate_function}({self.table_alias}.{self.name})'
      else:
        result = f"{self.table_alias}.{self.name}"

    if self.select_alias:
      result += ' as ' + self.select_alias

    return result