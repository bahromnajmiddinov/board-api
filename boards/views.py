from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Board
from .serializers import BoardSerializer


class BoardAPIView(APIView):

    def get(self, request):
        boards = Board.objects.all()
        serializer = BoardSerializer(boards, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = BoardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class BoardDetailAPIView(APIView):
    
    def get_object(self, pk):
        try:
            return Board.objects.get(pk=pk)
        except Board.DoesNotExist:
            return Response(status=404)
    
    def get(self, request, pk):
        board = self.get_object(pk)
        serializer = BoardSerializer(board)
        return Response(serializer.data)
    
    def put(self, request, pk):
        board = self.get_object(pk)
        serializer = BoardSerializer(board, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    def patch(self, request, pk):
        board = self.get_object(pk)
        serializer = BoardSerializer(board, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    def delete(self, request, pk):
        board = self.get_object(pk)
        board.delete()
        return Response(status=204)
    
    