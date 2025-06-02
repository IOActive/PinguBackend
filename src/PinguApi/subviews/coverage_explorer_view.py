import zipfile
import io
from django.http import FileResponse, StreamingHttpResponse
from rest_framework.views import APIView
import os
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.conf import settings 
from rest_framework.exceptions import APIException, NotAcceptable, NotFound

from PinguApi.tasks import get_coverage_artifacts_package, generate_coverage_html_report, get_coverage_html_report
from PinguApi.submodels.project import Project
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

class CoverageExplorerView(APIView):
    """This view is used to explore coverage data for a project. Returns a JSON object which contains the html reports encoded as base64."""
    authentication_classes = [SessionAuthentication, TokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name="project_id",
                in_=openapi.IN_QUERY,  # Query parameter
                description="Project ID",
                required=True,
                type=openapi.TYPE_STRING
            )
        ]
    )
    def get(self, request, *args, **kwargs):
        project_id = request.query_params.get('project_id')
        if not project_id:
            raise NotAcceptable("Project ID is required")
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            raise NotFound("Project not found")
        
        # Get the coverage data from the project
        # This is a placeholder for where you would get the coverage data
        try:
            json_result = generate_coverage_html_report.apply(args=[project]).get()
            response = Response(data=json_result, status=200, content_type='application/json')
            return response
        except Exception as e:
            raise APIException(detail="Failed to get coverage data", code=500)

class CoverageDownloadView(APIView):
    """Zips all files in the tmp folder and returns the zip"""
    
    authentication_classes = [SessionAuthentication, TokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]

    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name="artifacts",
                in_=openapi.IN_QUERY,  # Query parameter
                description="Coverage Artifacts",
                required=False,
                type=openapi.TYPE_BOOLEAN
            ),
            openapi.Parameter(
                name="report",
                in_=openapi.IN_QUERY,  # Query parameter
                description="Report name",
                required=False,
                type=openapi.TYPE_STRING
            ),
            
        ]
    )
    def get(self, request, *args, **kwargs):
        try:           
            project_id = self.kwargs['pk']
            artifacts_flag = request.GET.get('artifacts', False)
            report_name = request.GET.get('report', None)
            
            try:
                project = Project.objects.get(id=project_id)
            except Project.DoesNotExist:
                raise NotFound(detail="Project not found", code=404)
            
            if artifacts_flag:
                try:
                    zip_stream = get_coverage_artifacts_package.apply(args=[project]).get()
                except Exception as e:
                    raise APIException(detail="Failed to generate coverage report", code=500)

                response = FileResponse(zip_stream, content_type="application/zip")
                response["Content-Disposition"] = f'attachment; filename="{project.name}_coverage.zip"'
                return response
            
            if report_name:
                try:
                    report_stream = get_coverage_html_report.apply(args=[project, report_name]).get()
                    if not report_stream:
                        raise NotFound(detail="Report not found", code=404)
                    response = StreamingHttpResponse(self.stream_large_html_file(report_stream), content_type="text/html")
                    return response
                except Exception as e:
                    raise APIException(detail="Failed to generate coverage html report", code=500)

        except Exception as e:
            return APIException(detail="Unable to create zip file", code=500)
        
    def stream_large_html_file(self, report_stream):
        """Generator that reads the file in chunks"""
        while chunk := report_stream.read(8192):  # 8KB chunks
            yield chunk
