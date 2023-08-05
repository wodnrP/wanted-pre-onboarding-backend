from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.authentication import get_authorization_header
from user.authentication import decode_access_token
from .models import Board
from .serializer import BoardSerializer
# Create your views here.

class BoardAPIView(APIView):
    # 게시글 작성
    def post(self, request):
        auth = get_authorization_header(request).split()
        if auth and len(auth) == 2:
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
        auth = get_authorization_header(request).split()
        if auth and len(auth) == 2:
            board = Board.objects.get(pk = board_id)
            # 해당 게시글 작성자인지 확인
            if decode_access_token(auth[1]) == board.user_id:
                serializer = BoardSerializer(board, data=request.data, partial=True)
                
                if serializer.is_valid():
                    serializer.save(data=request.data, request=request)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            else:
                return Response({'Message':'해당 게시글 작성자가 아닙니다.'}, status=status.HTTP_401_UNAUTHORIZED)

    # 특정 게시글 삭제 
    def delete(self, request, board_id):
        auth = get_authorization_header(request).split()
        if auth and len(auth) == 2:
            board = Board.objects.get(pk = board_id)
            if decode_access_token(auth[1]) == board.user_id:
                board.delete()
                return Response({'Message':'Success'}, status=status.HTTP_200_OK)
            else:
                return Response({'Message':'해당 게시글 작성자가 아닙니다.'}, status=status.HTTP_401_UNAUTHORIZED)
    