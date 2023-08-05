from django.urls import path
from .views import BoardAPIView, BoardDetailAPIView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', BoardAPIView.as_view(), name="PostBoardAPI"),
    path('<int:board_id>', BoardDetailAPIView.as_view(), name="GetUpdateDeleteBoardAPI"),
    path('', BoardAPIView.as_view(), name="GetAllBoardAPI"),
    ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)