from rest_framework.response import Response
from rest_framework.views import APIView

from boards.models import Board, Project
from boards.serializers import BoardSerializer, ProjectSerializer
from .serializers import TeamSerializer
from .models import Team


class TeamAPIView(APIView):
    
    def get(self, request):
        type = request.GET.get('type', 'all')
        
        if type == 'myTeams':
            teams = Team.objects.filter(members_in=[request.user])
        else:
            if request.user.is_staff:
                teams = Team.objects.all()
            else:
                return Response({'detail': 'You are not allowed to this action.'}, status=403)
        
        serializer = TeamSerializer(teams, many=True, context={'request': request})
        return Response(serializer.data)
    
    def post(self, request):
        serializer = TeamSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class TeamDetailAPIView(APIView):
    def get_object(self, pk):
        return Team.objects.get(pk=pk)
    
    def get(self, request, pk):
        team = self.get_object(pk)
        serializer = TeamSerializer(team, context={'request': request})
        data = {
            'team': serializer.data,
            'boards': BoardSerializer(team.team_boards.all(), many=True).data,
            'projects': ProjectSerializer(team.team_projects.all(), many=True).data,
        }
        return Response(data=data)
    
    def put(self, request, pk):
        team = self.get_object(pk)
        serializer = TeamSerializer(team, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    def delete(self, request, pk):
        team = self.get_object(pk)
        team.delete()
        return Response(status=204)
    
    def patch(self, request, pk):
        team = self.get_object(pk)
        serializer = TeamSerializer(team, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    