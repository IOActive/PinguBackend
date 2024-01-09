from rest_framework import serializers 
from PinguApi.submodels.Trial import Trial

class TrialSerializer(serializers.ModelSerializer):

    class Meta:
        model = Trial
        fields = ('id',
                  'app_name',
                  'probability',
                  'app_args'
                  )