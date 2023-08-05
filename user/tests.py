from django.test import (TestCase, Client)
import json
from django.urls import reverse
from rest_framework.test import APIClient
from .models import User
# Create your tests here.

#회원가입 기능 관련 테스트케이스
class SignupTest(TestCase):
    # 테스트에 필요한 객체를 미리 생성
    def setUp(self):
        pass

    # 테스트 과정 중에 생긴 데이터 제거 
    # 다른 테스트와 연관성이 있어도 정확한 테스트 결과를 위해 Clean UP을 진행
    def tearDown(self):
        User.objects.all().delete()
    
    # 회원가입 기능이 성공적으로 동작하는지 테스트
    def test_signup_post_success(self):
        client = Client()

        signup_info = {
            "email" : "signTestUser@test.com",
            "password" : "test12346",
            "nickname" : "테스트사용자"
        }
        # json.dumps()로 객체를 json화 시켜줌
        response = client.post(reverse('signup'), json.dumps(signup_info), content_type='application/json')
        
        # assertEqual()로 response 받은 status code가 정상적인지 확인
        self.assertEqual(response.status_code, 201)

# 로그인 기능 관련 테스트케이스
class LoginTest(TestCase):
    def setUp(self):
        self.url = reverse('login')
        self.user = User.objects.create(
            email="loginTestUser@test.com",
            nickname="로그인테스트사용자"
        )
        self.user.set_password("test09876")
        self.user.save()

    def tearDown(self):
        User.objects.all().delete()

    # 로그인 기능 테스트
    def test_login_post_sucess(self):
        login_info = {
            "email" : "loginTestUser@test.com",
            "password" : "test09876"
        }
        response = self.client.post(self.url, data=login_info, format='json')
        self.assertEqual(response.status_code, 201)
    
    # 로그인시 이메일이 틀렸을 경우 에러 테스트
    def test_login_post_invalid_username(self):
        login_info = {
            "email" : "loginTest@test.com",
            "password" : "test09876"
        }
        response = self.client.post(self.url, data=login_info, format='json')
        self.assertEqual(response.status_code, 400)
    
    # 로그인시 비밀번호가 틀렸을 경우 에러 테스트
    def test_login_post_invalid_password(self):
        login_info = {
            "email" : "loginTestUser@test.com",
            "password" : "test12345"
        }
        response = self.client.post(self.url, data=login_info, format='json')
        self.assertEqual(response.status_code, 400)

# 로그아웃 테스트 케이스
class LogoutTest(TestCase):
    """
    1. json massage, status=200이 정상적으로 반환되는지 테스트
    2. 리프레시 토큰이 쿠키에서 삭제되었는지 테스트
    """ 
    def test_logout_delete_success(self):
        response = self.client.delete(reverse('logout'), format='json')

        self.assertEqual(response.json(), {'Message' : 'Logout success'} ) # json 메시지 확인
        self.assertEqual(response.status_code, 200)                        # status code 200 확인
        self.assertEqual(response.cookies['refreshToken'].value, "")       # 쿠키에 refreshToken 값 확인 



