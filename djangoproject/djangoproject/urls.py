from django.contrib import admin
from django.urls import path,include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/',include('user.urls'), name='user'),
    path('article/', include('article.urls'), name='article'),
    path('navigation/', include('navigation.urls')),
]