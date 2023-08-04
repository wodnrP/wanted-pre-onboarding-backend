from django.urls import path
from .views import BoardAPIView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', BoardAPIView.as_view(), name="GetAllBoardAPI"),
    ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)