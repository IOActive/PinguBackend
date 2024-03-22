from rest_framework import serializers 
from PinguApi.submodels.Statistic import Statistic
from PinguApi.submodels.Job import Job
class StatisticSerializer(serializers.ModelSerializer):
    job_id = serializers.PrimaryKeyRelatedField(many=False, required=True, queryset=Job.objects.all())

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