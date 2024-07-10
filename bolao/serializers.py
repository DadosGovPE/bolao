from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Team, Game, Bet

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'name']

class GameSerializer(serializers.ModelSerializer):
    team1 = TeamSerializer(read_only=True)
    team2 = TeamSerializer(read_only=True)
    team1_id = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all(), write_only=True, source='team1')
    team2_id = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all(), write_only=True, source='team2')

    class Meta:
        model = Game
        fields = ['id', 'team1', 'team2', 'team1_id', 'team2_id', 'date']

class BetSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    game = GameSerializer(read_only=True)
    game_id = serializers.PrimaryKeyRelatedField(queryset=Game.objects.all(), write_only=True, source='game')

    class Meta:
        model = Bet
        fields = ['id', 'user', 'game', 'game_id', 'team1_score', 'team2_score', 'created_at']
