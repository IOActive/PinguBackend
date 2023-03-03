from rest_framework import serializers 
from PinguApi.submodels.Job import Job

class JobSerializer(serializers.ModelSerializer):
    template = serializers.PrimaryKeyRelatedField(many=False, read_only=True)

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