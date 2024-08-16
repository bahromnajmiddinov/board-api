from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from drf_spectacular.utils import extend_schema

from .models import Board, Project
from .serializers import BoardSerializer, ProjectSerializer


@extend_schema(tags=["Boards"])
class BoardAPIView(APIView):

    @extend_schema(
        summary="Retrieve all boards",
        description="This endpoint retrieves a list of all available boards.",
        responses={200: BoardSerializer(many=True)},
    )
    
    def get(self, request):
        boards = Board.objects.all()
        serializer = BoardSerializer(boards, many=True)
        return Response(serializer.data)
    
    @extend_schema(
        summary="Create a new board",
        description="This endpoint allows for the creation of a new board.",
        request=BoardSerializer,
        responses={201: BoardSerializer, 400: 'Bad Request'}
    )
    
    def post(self, request):
        serializer = BoardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@extend_schema(tags=["Boards"])
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


class ProjectAPIView(ListCreateAPIView):
    serializer_class = ProjectSerializer
    
    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)


class ProjectDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()
    