from rest_framework import serializers 
from PinguApi.submodels.TestCase import TestCase
from PinguApi.submodels.DataBundle import DataBundle
 
class DataBundleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataBundle
        fields = ('id',
                  'name',
                  'bucket_name',
                  'source',
                  'is_local',
                  'timestamp',
                  'sync_to_worker'
                  )