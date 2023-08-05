from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse

from .models import Board
from user.models import User
# Create your tests here.

# 게시판 CR 테스트
class BoardTest(TestCase):
    def setUp(self):
        self.client = APIClient(enforce_csrf_checks=True)
        self.maxDiff = None
        
        # 사용자 정보 생성
        self.user = User.objects.create(
            id = 1,
            email = "BoardTestUser@test.com",
            nickname = "테스트사용자",
        )
        self.user.set_password('asdf12345')
        self.user.save()

        # 게시판 정보 생성
        self.url = reverse('GetAllBoardAPI')
        self.board = Board.objects.create(
            id=1,
            user_id=1,
            title="TestTitle",
            contents="TestContents"
        )
        self.board.save()

    def tearDown(self):
        Board.objects.all().delete()
        User.objects.all().delete()
    
    # 게시글 전체 조회 기능 테스트
    def test_all_get_success(self):
        response = self.client.get(self.url, content_type='application/json')
        self.assertEqual(response.status_code, 200)

    # 게시글 작성 기능 테스트 
    def test_create_post_success(self):
        login_user = {
            "email" : "BoardTestUser@test.com",
            "password" : "asdf12345",
        }
        # 사용자 로그인
        login_response = self.client.post(reverse('login'), 
        data=login_user, format='json')
        
        # 로그인한 사용자의 access_token을 header에 인증
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {login_response.json()['access_token']}"
        )

        board_info = {
            "title" : "Test제목",
            "contents" : "Test내용"
        }
        response = self.client.post(reverse('PostBoardAPI'), data=board_info, format='json')
        self.assertEqual(response.status_code, 201)

# 특정 게시판 RUD 기능 테스트
class BoardDetailTest(TestCase):
    def setUp(self):
        self.client = APIClient(enforce_csrf_checks=True)
        self.maxDiff = None

        self.user = User.objects.create(
            id = 1,
            email = "BoardTestUser@test.com",
            nickname = "테스트사용자",
        )
        self.user.set_password('asdf12345')
        self.user.save()
        # 게시글 id 값 url에 추가
        board_id=1
        self.url = reverse('GetUpdateDeleteBoardAPI', args=[board_id])
        self.board = Board.objects.create(
            id=1,
            user_id=1,
            title="TestTitle",
            contents="TestContents"
        )
        self.board.save()
    
    def tearDown(self):
        Board.objects.all().delete()
    
    # 특정 게시글 조회 기능 테스트
    def test_detail_get_success(self):
        response = self.client.get(self.url, content_type='application/json')
        self.assertEqual(response.status_code, 200)
    
    # 특저 게시글 수정 기능 테스트
    def test_detail_patch_success(self):
        # 사용자 로그안
        login_user = {
            "email" : "BoardTestUser@test.com",
            "password" : "asdf12345",
        }
        # 사용자 로그인
        login_response = self.client.post(reverse('login'), 
        data=login_user, format='json')
        
        # 로그인한 사용자의 access_token을 header에 인증
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {login_response.json()['access_token']}"
        )

        board_update = {
            "title" : "Test제목수정"
        }
        response = self.client.get(self.url, board_update)
        self.assertEqual(response.status_code, 200)
    
    # 특정 게시글 삭제 기능 테스트
    def test_detail_delete_success(self):
        # 사용자 로그인
        login_user = {
            "email" : "BoardTestUser@test.com",
            "password" : "asdf12345",
        }
        # 사용자 로그인
        login_response = self.client.post(reverse('login'), 
        data=login_user, format='json')
        
        # 로그인한 사용자의 access_token을 header에 인증
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {login_response.json()['access_token']}"
        )

        response = self.client.delete(self.url)
        # 응답 상태코드를 확인, 성공 확인
        self.assertEqual(response.status_code, 200)

        # 삭제된 객체가 존재하지 않는지 확인
        with self.assertRaises(Board.DoesNotExist):
            self.board.refresh_from_db()