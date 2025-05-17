from rest_framework import serializers
from .models import Player, Team

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'

class PlayerSerializer(serializers.ModelSerializer):
    currentTeamAbbrev = serializers.CharField(source='currentTeamID.triCode', read_only=True)
    teamLogo = serializers.CharField(source='currentTeamID.teamLogo', read_only=True)
    
    class Meta:
        model = Player
        fields = '__all__'