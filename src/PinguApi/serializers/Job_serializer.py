from rest_framework import serializers 
from PinguApi.submodels.Job import Job
from PinguApi.submodels.JobTemplate import JobTemplate
class JobSerializer(serializers.ModelSerializer):
    template = serializers.PrimaryKeyRelatedField(many=False, required=False, queryset=JobTemplate.objects.all())

    class Meta:
        model = Job
        fields = ('id',
                  'name',
                  'description',
                  'project',
                  'date',
                  'enabled',
                  'archived',
                  'platform',
                  'environment_string',
                  'template',
                  'custom_binary_path',
                  'custom_binary_filename',
                  'custom_binary_revision'
                  )