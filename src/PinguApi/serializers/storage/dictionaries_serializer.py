from rest_framework import serializers


class GetDictionarySerializer(serializers.Serializer):
    project_id = serializers.CharField(required=True)
    fuzztarget_id = serializers.CharField(required=True)
    dictionary_name = serializers.CharField(required=False)
    

class UploadDictionarySerializer(serializers.Serializer):
    project_id = serializers.CharField(required=True)
    fuzztarget_id = serializers.CharField(required=True)
    dictionary = serializers.FileField(required=True)