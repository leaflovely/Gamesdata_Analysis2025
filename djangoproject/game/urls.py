from django.urls import path
from .views import GetGameAPIView, SearchGameAPIView, PublishGameAPIView

app_name = 'Game'

urlpatterns = [
    path('get', GetGameAPIView.as_view(), name='get_Game'),
    path('search', SearchGameAPIView.as_view(), name='search_Game'),
    path('publish', PublishGameAPIView.as_view(), name='publish_Game'),
]
