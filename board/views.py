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
    def get(self, request):
        paginator = PageNumberPagination()
        paginator.page_size = 10
        
        items = request.GET.get('items', None)
        page = request.GET.get('page', None)

        if page is None:
            page = 1

        if items is not None:
            paginator.page_size = int(items)

        page = int(page)
        board_object = Board.objects.all()
        count = board_object.count()
        page_data = count % paginator.page_size 

        if count <= paginator.page_size:
            total_page = 1

        elif page_data == 0:
            total_page = count / paginator.page_size

        else:
            total_page = count / paginator.page_size + 1
        total_page = math.floor(total_page)
        is_next = total_page - page > 0


        board = board_object.order_by('create_time')
        result = paginator.paginate_queryset(board, request)
        
        try:
            serializer = BoardSerializer(result, many = True, context={"request": request})
            result_serializer = serializer.data
            
            pagenation = {
                "total_page" : total_page,
                "current_page" : page,
                "total_count" : count,
                "is_next" : is_next,
                "result" : result_serializer
            }
            
            return Response(pagenation, status=status.HTTP_200_OK)
        
        except board.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, board_id):
        try:
            board = Board.objects.get(pk = board_id)
            serializer = BoardSerializer(board, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except board.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, board_id):
        pass

    def delete(self, request, board_id):
        pass
    
    def post(self, request):
        pass