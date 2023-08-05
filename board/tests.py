from django.test import (TestCase, Client)
import json
from django.urls import reverse
from .models import Board

# Create your tests here.

# 게시판 CR 테스트
class BoardTest(TestCase):
    def setUp(self):
        self.url = reverse('GetAllBoardAPI')
        self.board = Board.objects.create(
            id=1,
            title="TestTitle",
            contents="TestContents"
        )
        self.board.save()

    def tearDown(self):
        Board.objects.all().delete()

    # 게시글 전체 조회 기능 테스트
    def test_all_get_success(self):
        response = self.client.get(self.url, content_type='application/json')
        self.assertEqual(response.status_code, 200)

    # 게시글 작성 기능 테스트 
    def test_create_post_success(self):
        board_info = {
            "title" : "Test제목",
            "contents" : "Test내용"
        }
        response = self.client.post(reverse('PostBoardAPI'), data=board_info, format='json')
        self.assertEqual(response.status_code, 201)

# 특정 게시판 RUD 기능 테스트
class BoardDetailTest(TestCase):
    def setUp(self):
        # 게시글 id 값 url에 추가
        board_id=1
        self.url = reverse('GetUpdateDeleteBoardAPI', args=[board_id])
        self.board = Board.objects.create(
            id=1,
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
        board_update = {
            "title" : "Test제목수정"
        }
        response = self.client.get(self.url, board_update)
        self.assertEqual(response.status_code, 200)
    
    # 특정 게시글 삭제 기능 테스트
    def test_detail_delete_success(self):
        response = self.client.delete(self.url)

        # 응답 상태코드를 확인, 성공 확인
        self.assertEqual(response.status_code, 200)

        # 삭제된 객체가 존재하지 않는지 확인
        with self.assertRaises(Board.DoesNotExist):
            self.board.refresh_from_db()