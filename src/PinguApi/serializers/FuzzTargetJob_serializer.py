from rest_framework import serializers 
from PinguApi.submodels.FuzzTargetJob import FuzzTargetJob
from PinguApi.submodels.FuzzTarget import FuzzTarget
from PinguApi.submodels.Job import Job
from PinguApi.submodels.Fuzzer import Fuzzer

class FuzzTargetJobSerializer(serializers.ModelSerializer):
    fuzzing_target = serializers.PrimaryKeyRelatedField(many=False, required=True, queryset=FuzzTarget.objects.all())
    job = serializers.PrimaryKeyRelatedField(many=False, required=True, queryset=Job.objects.all())
    engine = serializers.PrimaryKeyRelatedField(many=False, required=True, queryset=Fuzzer.objects.all())
    
    class Meta:
        model = FuzzTargetJob
        fields = ('id',
                  'fuzzing_target',
                  'job',
                  'engine',
                  'weight',
                  'last_run'
                  )