from rest_framework import serializers

from accounts.serializers import CustomUserSerializer
from .models import Team


class TeamSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='team-detail')
    owner = serializers.HyperlinkedRelatedField(many=False, read_only=True, view_name='user-detail')
    members = CustomUserSerializer(many=True, read_only=True)
    class Meta:
        model = Team
        fields = '__all__'
        extra_fields = ['url']
