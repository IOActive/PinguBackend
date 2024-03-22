from rest_framework.routers import SimpleRouter
#from PinguApi.subviews.Authentication_view import UserViewSet
from PinguApi.subviews.Authentication_view import LoginViewSet, RegistrationViewSet, RefreshViewSet


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