from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from . import views


urlpatterns = [
    path('', views.TrackList.as_view()),
    path('<int:pk>/', views.TrackDetail.as_view()),
    path('add-my-songs/<int:pk>/', views.AddMySongs.as_view()),
    path('my-songs/', views.MySongs.as_view()),
    
    path('auth/', include("rest_framework.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)