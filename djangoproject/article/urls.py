from django.urls import path
from .views import GetArticleAPIView, SearchArticleAPIView, PublishArticleAPIView

app_name = 'article'

urlpatterns = [
    path('get', GetArticleAPIView.as_view(), name='get_article'),
    path('search', SearchArticleAPIView.as_view(), name='search_article'),
    path('publish', PublishArticleAPIView.as_view(), name='publish_article'),
]
