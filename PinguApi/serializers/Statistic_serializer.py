from rest_framework import serializers 
from PinguApi.submodels.Statistic import Statistic

class StatisticSerializer(serializers.ModelSerializer):
    job_id = serializers.PrimaryKeyRelatedField(many=False, read_only=True)

    class Meta:
        model = Statistic
        fields = ('id',
                  'job_id',
                  'iteration',
                  'runtime',
                  'execs_per_sec',
                  'date',
                  'last_beat_time',
                  'status',
                  'task_payload'
                  )