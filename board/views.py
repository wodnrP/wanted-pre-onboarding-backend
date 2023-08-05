from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from .models import Board
from .serializer import BoardSerializer
from django.db.models import Count
import math
# Create your views here.

class BoardAPIView(APIView):
    # 게시글 작성
    def post(self, request):
        serializer = BoardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        page = request.GET.get('page', None)
        items = request.GET.get('items', None)
        
        paginator = PageNumberPagination()
        # 1페이지 최대 items 수 = 10
        paginator.page_size = 10

        # defalt paeg = 1
        if page is None:
            page = 1
        
        # items가 null이 아닐 경우, items 값으로 page_size 초기화 
        if items is not None:
            paginator.page_size = int(items)
        
        # page 값 int로 타입 변환
        page = int(page)
        
        board = Board.objects.filter().order_by('-create_time')
        result = paginator.paginate_queryset(board, request)
        
        try:
            serializer = BoardSerializer(result, many = True, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Board.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    

class BoardDetailAPIView(APIView):
    # 특정 게시글 조회 
    def get(self, request, board_id):
        try:
            board = Board.objects.get(pk = board_id)
            serializer = BoardSerializer(board, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Board.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    
    # 특정 게시글 수정
    def patch(self, request, board_id):
        board = Board.objects.get(pk = board_id)
        serializer = BoardSerializer(board, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save(data=request.data, request=request)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 특정 게시글 삭제 
    def delete(self, request, board_id):
        board = Board.objects.get(pk = board_id)
        board.delete()
        return Response({'Message':'Success'}, status=status.HTTP_200_OK)
    