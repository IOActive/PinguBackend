from rest_framework import serializers 
from PinguApi.submodels.BuildMetadata import BuildMetadata
 
 
class BuildMetadataSerializer(serializers.ModelSerializer):
    job = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    class Meta:
        model = BuildMetadata
        fields = ('id',
                  'job',
                  'revision',
                  'bad_build',
                  'console_output',
                  'bot_name',
                  'symbols',
                  'timestamp'
                  )