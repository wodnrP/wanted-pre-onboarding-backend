from django.urls import path
from .views import SignupAPIView, LoginAPIView, LogoutAPIView, RefreshAPIView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('signup', SignupAPIView.as_view(), name='signup'),         # 회원가입
    path('login', LoginAPIView.as_view(), name='login'),            # 로그인
    path('logout', LogoutAPIView.as_view(), name='logout'),         # 로그아웃
    path('refresh', RefreshAPIView.as_view(), name='refresh'),      # refresh_token으로 토큰 갱신
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)