import uuid
from PinguApi.submodels.crash_stats import CrashStats
from django.db.models import Count, Min, Max, Sum, Case, When, Value, BooleanField
from django.db.models.functions import Power
from django.db.models.aggregates import Sum


def crash_stats_handler(start_time, end_time, interval, group_by_fields, project_id):
    # Query the database using extracted parameters
    query = CrashStats.objects.all()

    if start_time:
        query = query.filter(time__gte=start_time)
    if end_time:
        query = query.filter(time__lte=end_time)
    if project_id:
        query = query.filter(project=project_id)

    # Dynamically add group_by fields to `.values()` and `.annotate()`

    query_fields = [
        'crash_type', 'crash_state', 'security_flag', 'fuzzer',
        'job', 'revision', 'platform', 'project', 'reproducible_flag', 'crash', 'testcase', 'time'
    ]

    # Group by the fields in `group_by_fields`
    group_by_fields = [field for field in group_by_fields if field in query_fields]

    # Perform the aggregation based on dynamic grouping
    query = query.time_bucket('time', interval).values(*group_by_fields).annotate(
        crashes_count=Count('id'),
        min_crash_time_in_ms=Min('crash_time_in_ms'),
        max_crash_time_in_ms=Max('crash_time_in_ms'),
        sum_crash_time_in_ms=Sum('crash_time_in_ms'),
        sum_square_crash_time_in_ms=Sum(Power('crash_time_in_ms', 2)),
        new_flag=Max(
            Case(
                When(new_flag=True, then=Value(1)),
                default=Value(0),
                output_field=BooleanField()
            )
        ),
    )

    # Create columns based on the fields in your `values` and `annotate`
    cols = []
    for group_by_field in group_by_fields:
        cols.append({"label": f"{group_by_field}", "type": "string"})
    cols += [
        {"label": "crashes_count", "type": "number"},
        {"label": "min_crash_time_in_ms", "type": "number"},
        {"label": "max_crash_time_in_ms", "type": "number"},
        {"label": "sum_crash_time_in_ms", "type": "number"},
        {"label": "sum_square_crash_time_in_ms", "type": "number"},
        {"label": "new_flag", "type": "boolean"}
    ]
    
    rows = []
    for result in query:
        cel = {"c": []}
        for field in group_by_fields:
            if result[field] is not None:
                cel['c'].append({"v": str(result[field])})
            else: 
                cel['c'].append({"v": "N/A"})

        cel['c'].append({"v": result["crashes_count"]})  # Example replacement for 'tests_executed'
        cel['c'].append({"v": result["min_crash_time_in_ms"] or 0.0}),
        cel['c'].append({"v": result["max_crash_time_in_ms"] or 0.0}),
        cel['c'].append({"v": result["sum_crash_time_in_ms"] or 0.0}),
        cel['c'].append({"v": result["sum_square_crash_time_in_ms"] or 0.0}),
        cel['c'].append({"v": result["new_flag"]}),
        rows.append(cel)
        
    # Prepare the JSON structure
    return {
        'cols': cols,
        'rows': rows,
        "column_descriptions": {}
    }