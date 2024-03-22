from rest_framework import serializers 
from PinguApi.submodels.FuzzTarget import FuzzTarget
from PinguApi.submodels.Fuzzer import Fuzzer

class FuzzTargetSerializer(serializers.ModelSerializer):
    fuzzer_engine = serializers.PrimaryKeyRelatedField(many=False, required=True, queryset=Fuzzer.objects.all())
    class Meta:
        model = FuzzTarget
        fields = ('id',
                  'fuzzer_engine',
                  'project',
                  'binary'
                  )