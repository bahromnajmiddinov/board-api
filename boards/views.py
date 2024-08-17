from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.decorators import api_view

from drf_spectacular.utils import extend_schema, OpenApiParameter

from teams.models import Team
from .models import Board, Project
from .serializers import BoardSerializer, ProjectSerializer


@extend_schema(tags=["Boards"])
class BoardAPIView(APIView):

    @extend_schema(
        summary="Retrieve all boards",
        description="This endpoint retrieves a list of all available boards.",
        parameters=[
            OpenApiParameter(name='type', description='Get public or requested user`s boards,' \
                             'default public, public|private', required=False, type=str),
            OpenApiParameter(name='starred', description='Get user`s starred boards, true|false', required=False, type=str),
            OpenApiParameter(name='team_id', description='Get boards of a specific team, team_id', required=False, type=int),
        ],
        responses={200: BoardSerializer(many=True)},
    )
    
    def get(self, request):
        type = request.GET.get('type', 'public')
        starred = request.GET.get('starred', 'false')
        team_id = request.GET.get('team_id', None)
        
        if type == 'private':
            boards = Board.objects.filter(participants_in=[request.user])
        elif type == 'public':
            boards = Board.objects.filter(is_public=True)
        
        if team_id:
            boards = boards.filter(participants_in=[request.user], teams__id=team_id)
        
        if starred == 'true':
            boards = boards.filter(participants_in=[request.user], starred_by__user=request.user)

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


@api_view(['POST'])
def add_board_to_project(request, project_id, board_id):
    project = Project.objects.get(pk=project_id, owner=request.request.user)
    board = Board.objects.get(pk=board_id, created_by=request.request.user)
    
    if board not in project.boards.all():
        project.boards.add(board)
        return Response(status=200)
    elif board in project.boards.all():
        project.boards.remove(board)
        return Response(status=200)
    
    return Response(status=400)


@api_view(['POST'])
def star_board(request, board_id):
    board = Board.objects.get(pk=board_id, participants_in=[request.request.user])
    
    if board.starred_by.filter(user=request.request.user).exists():
        board.starred_by.remove(request.request.user)
    else:
        board.starred_by.add(request.request.user)
        board.save()
    
    return Response(status=200)

    