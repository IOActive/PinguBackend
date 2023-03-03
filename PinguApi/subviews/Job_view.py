from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
 
from PinguApi.submodels.Job import Job
from PinguApi.serializers.Job_serializer import JobSerializer
from rest_framework.decorators import api_view

from rest_framework import generics
from rest_framework.permissions import IsAdminUser

class JobList(generics.ListAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAdminUser]
    
#@api_view(['GET'])
#def list_all_jobs(request):
#    # find tutorial by pk (id)
#    try: 
#        jobs = Job.objects
#        job_serializer = JobSerializer(jobs, many=True)
#        return JsonResponse(job_serializer.data, safe=False)
#    except Tutorial.DoesNotExist: 
#        return JsonResponse({'message': 'The tutorial does not exist'}, status=status.HTTP_404_NOT_FOUND) 