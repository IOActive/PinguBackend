# Copyright 2024 IOActive
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from rest_framework.response import Response
from PinguApi.submodels.crash_stats import CrashStats
from PinguApi.serializers.crash_stats_serializer import CrashStatsSerializer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import NotAcceptable, APIException
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.utils.dateparse import parse_datetime
from PinguApi.handlers.crash_stats import crash_stats_handler
from PinguApi.submodels.project import Project

class CrashStats_List_Create_APIView(generics.mixins.ListModelMixin, 
                      generics.mixins.CreateModelMixin,
                      generics.GenericAPIView):
    
    authentication_classes = [SessionAuthentication, TokenAuthentication, JWTAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'project_id']
    serializer_class = CrashStatsSerializer
    
    queryset = CrashStats.objects.all()
    paginator = None
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name="start_date",
                in_=openapi.IN_QUERY,  # Query parameter
                description="Start time for filtering (format: YYYY-MM-DD HH:MM:SS)",
                required=False,
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                name="end_date",
                in_=openapi.IN_QUERY,
                description="End time for filtering (format: YYYY-MM-DD HH:MM:SS)",
                required=False,
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                name="interval",
                in_=openapi.IN_QUERY,
                description="Time interval for bucketing (e.g., '1 hour', '1 day')",
                required=False,
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                name="group_by",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_ARRAY,
                items=openapi.Items(type=openapi.TYPE_STRING),
                description="Fields to group by (comma-separated list)",
                required=True
            ),
        ]
    )
    def get(self, request, *args, **kwargs):
        try:
            # Extract parameters from request
            start_date = request.query_params.get("start_date")
            end_date = request.query_params.get("end_date")
            interval = request.query_params.get("interval", "1 hour")  # Default to 1 hour if not provided
            group_by_param = request.query_params.getlist("group_by", [])  # List of fields to group by
            project_id = request.query_params.get("project_id", None)
            
            try:
                if project_id:
                    project = Project.objects.get(id=project_id)
            except Exception as e:
                raise FileNotFoundError(details="THe provided project ID does not exists", code=404)
            
            # If the group_by parameter contains a single string with commas, split it into a list
            if len(group_by_param) == 1 and ',' in group_by_param[0]:
                group_by_fields = group_by_param[0].split(',')
            else:
                group_by_fields = group_by_param  # Already a list of fields

            # Convert start_time and end_time to proper datetime if needed
            if start_date:
                start_date = parse_datetime(start_date)
            if end_date:
                end_date = parse_datetime(end_date)

            # Ensure start_time and end_time are valid
            if start_date and end_date and start_date > end_date:
                raise NotAcceptable(detail="start_time cannot be greater than end_time", status=406)
            
            # Ensure that at least one valid field is in the group-by
            if not group_by_fields:
                raise NotAcceptable(detail="You must specify at least one valid group_by field.", code=406)

            # List of allowed group-by fields (should match your model fields)
            allowed_group_by_fields = [
                'crash_type', 'crash_state', 'security_flag', 'fuzzer',
                'job', 'revision', 'platform', 'project', 'reproducible_flag', 'crash', 'testcase', 'time'
            ]

            # Filter out invalid group_by fields
            invalid_group_by_fields = [field for field in group_by_fields if field not in allowed_group_by_fields]
            if invalid_group_by_fields:
                raise NotAcceptable(detail=f"Invalid group_by fields: {', '.join(invalid_group_by_fields)}", code=406)

            response_data = crash_stats_handler(start_time=start_date, end_time=end_date, interval=interval, group_by_fields=group_by_fields, project_id=project_id)

            # Return the response as JSON
            response = Response({'success': True, 'detail': response_data})
            response.status_code = 200
            return response

        except Exception as e:
            raise APIException(detail=f"Failed to fetch the crash stats: {str(e)}", code=500)


    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)