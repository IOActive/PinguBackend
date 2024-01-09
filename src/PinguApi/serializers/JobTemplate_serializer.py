from rest_framework import serializers 
from PinguApi.submodels.JobTemplate import JobTemplate

class JobTemplateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = JobTemplate
        fields = ('id',
                  'name',
                  'environment_string'
                  )