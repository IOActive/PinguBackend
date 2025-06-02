
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

class PinguAPITestCase(APITestCase):
    databases = {'default', 'primary', 'bigquery'}  # Specify which databases to use in tests.
    
    @staticmethod
    def setup_user():
        User = get_user_model()
        return User.objects.create_user(
            'test',
            email='testuser@test.com',
            password='test'
    )
    