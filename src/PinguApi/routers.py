# Copyright 2024 IOActive
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from rest_framework.routers import SimpleRouter
#from PinguApi.subviews.Authentication_view import UserViewSet
from PinguApi.subviews.authentication_view import LoginViewSet, RegistrationViewSet, RefreshViewSet


routes = SimpleRouter()

# AUTHENTICATION
routes.register('auth/login', LoginViewSet, basename='auth-login')
routes.register('auth/register', RegistrationViewSet, basename='auth-register')
routes.register('auth/refresh', RefreshViewSet, basename='auth-refresh')

# USER
#routes.register(r'user', UserViewSet, basename='user')


urlpatterns = [
    *routes.urls
]