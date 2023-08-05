from django.urls import path
from .views import SignupAPIView, LoginAPIView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('signup', SignupAPIView.as_view(), name='signup'),         # 회원가입
    path('login', LoginAPIView.as_view(), name='login'),            # 로그인
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)