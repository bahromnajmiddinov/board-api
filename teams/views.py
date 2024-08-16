from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import TeamSerializer
from .models import Team


class TeamAPIView(APIView):
    
    def get(self, request):
        teams = Team.objects.all()
        serializer = TeamSerializer(teams, many=True)
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
        serializer = TeamSerializer(team)
        return Response(serializer.data)
    
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
    