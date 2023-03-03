from rest_framework import serializers 
from PinguApi.submodels.FuzzTargetJob import FuzzTargetJob

class FuzzTargetJobSerializer(serializers.ModelSerializer):
    fuzzing_target = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    job = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    engine = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    
    class Meta:
        model = FuzzTargetJob
        fields = ('id',
                  'fuzzing_target',
                  'job',
                  'weight',
                  'last_run'
                  )