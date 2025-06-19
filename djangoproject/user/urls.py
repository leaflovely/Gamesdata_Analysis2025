from django.urls import path
from .views import RegisterAPIView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('register', RegisterAPIView.as_view(), name='user'),
    path('login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/refresh', TokenRefreshView.as_view(), name='token_refresh'),
]
