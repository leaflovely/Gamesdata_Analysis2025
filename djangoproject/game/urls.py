from django.urls import path
from .views import GetGameAPIView, SearchGameAPIView, RatingAPIView, FilterGameAPIView

app_name = 'Game'

urlpatterns = [
    path('get', GetGameAPIView.as_view(), name='get_Game'),
    path('search', SearchGameAPIView.as_view(), name='search_Game'),
    path('rating', RatingAPIView.as_view(), name='rating_Game'),
    path('filter', FilterGameAPIView.as_view()),
]