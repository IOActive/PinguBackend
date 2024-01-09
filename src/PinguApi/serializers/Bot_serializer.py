from rest_framework import serializers 
from PinguApi.submodels.Bot import Bot
from PinguApi.utils.Base64FileField import Base64FileField

 
class BotSerializer(serializers.ModelSerializer):

    bot_logs = Base64FileField()
    class Meta:
        model = Bot
        fields = ('id',
                  'name',
                  'last_beat_time',
                  'task_payload',
                  'task_end_time',
                  'task_status',
                  'platform',
                  'blobstore_log_path',
                  'bot_logs',
                  )
