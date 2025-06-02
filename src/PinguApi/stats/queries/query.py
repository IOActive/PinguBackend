from PinguApi.stats.queries.group_by_query import QueryGroupBy, group_by_to_field_name


class Query:
    """Represents a stats query."""
  
    def __init__(self, query_fields, group_by, date_start,
                date_end, table_name, alias, interval="1 day", realted_fields=[], related_table=None):
        
        assert group_by is not None
        self.related_fields = realted_fields
        self.query_fields = query_fields
        self.group_by = group_by
        self.date_start = date_start
        self.date_end = date_end
        self.table_name = table_name
        self.alias = alias
        self.interval = interval
        self.related_talbe = related_table

    def _group_by_select(self):
        """Return a group by field."""
        if self.group_by == QueryGroupBy.GROUP_BY_INTERVAL:
            return None

        if self.group_by == QueryGroupBy.GROUP_BY_TIME:
            return 'time'

        return f"fuzzer_stats.{group_by_to_field_name(self.group_by)}"

    def _group_by(self):
        """Return the group by part of the query."""
        group_by = group_by_to_field_name(self.group_by)
        if group_by:
            if group_by != 'time':
                return f"fuzzer_stats.{group_by_to_field_name(self.group_by)}, interval"
            else:
                return f"{self.alias}.{group_by_to_field_name(self.group_by)}, interval"
        else:
            return 'interval'

    def _select_fields(self):
        """Return fields for the query."""
        group_by_select = self._group_by_select()
        fields = [group_by_select] if group_by_select else []

        for field in self.query_fields:
            fields.append(str(field))

        fields.append(f"time_bucket('{self.interval}', {self.alias}.time) as interval")
        return ', \n'.join(fields)

    def _where(self):
        """Return the where part of the query."""
        result = []
        if(self.related_fields):
            for related_field in self.related_fields:
                result.append(f"{self.related_talbe}.{related_field['name']} = '{related_field['value']}'\n")
        if self.date_end and self.date_start:
            result.append(f"{self.alias}.time > '{self.date_start}'::timestamptz\n")
            result.append(f"{self.alias}.time < '{self.date_end}'::timestamptz\n")
            result = ' AND '.join(result)
        if result:
            return f'WHERE  {result}'

        return ''

    def _join(self):
        return f"INNER JOIN fuzzer_stats ON {self.alias}.fuzzer_stats_id = fuzzer_stats.id"
    
    def _table_name(self):
        return f"{self.table_name} {self.alias}"
    
    def _format_field_list(self, fields):
        # If only one field, return it without comma
        group_field_alias = group_by_to_field_name(self.group_by)
        if len(fields) == 1:
            if group_field_alias is not None:
                return f"{group_field_alias}, {fields[0].select_alias},\n"
            else:
                return f"{fields[0].select_alias},\n"
        
        # For multiple fields, join with a comma and newline but omit the trailing comma
        if group_field_alias is not None:
            return f"{group_field_alias}, \n".join([f"{field.select_alias}" for field in fields])
        else:
            return ", \n".join([f"{field.select_alias}" for field in fields])

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

        return ' \n'.join(query_parts)

