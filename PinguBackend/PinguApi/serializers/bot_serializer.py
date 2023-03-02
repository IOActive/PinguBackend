from rest_framework import serializers 
from PinguApi.submodels.Bot import Bot
 
 
class BotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bot
        fields = ('id',
                  'bot_name',
                  'last_beat_time',
                  'task_payload',
                  'task_end_time',
                  'task_status',
                  'platform'
                  )
