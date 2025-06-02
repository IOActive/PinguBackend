from enum import Enum
from rest_framework import serializers

class GetBlobsSerializer(serializers.Serializer):
    project_id = serializers.CharField(required=True)
    key = serializers.CharField(required=True)
    

class UploadBlobsSerializer(serializers.Serializer):
    project_id = serializers.CharField(required=True)
    key = serializers.CharField(required=True)
    blob = serializers.FileField(required=True)
    metadata = serializers.CharField(required=False)