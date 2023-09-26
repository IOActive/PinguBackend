from drf_extra_fields.fields import Base64FileField
from logging import getLogger


class ZIPBase64File(Base64FileField):
    ALLOWED_TYPES = ['zip']
    
    class Meta:
        swagger_schema_fields = {
            'type': 'string',
            'title': 'File Content',
            'description': 'Content of the file base64 encoded',
            'read_only': True
        }

    def get_file_extension(self, filename, decoded_file):
        try:
            filename.split('.')[-1]
        except Exception as e:
            getLogger('PinguAPI').info(e)
        else:
            return 'zip'
            
     