from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *

class CampeonatoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campeonato
        fields = ['id', 'nome']

class BolaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bolao
        fields = ['id', 'nome', 'criado_em', 'criado_por', 'campeonato', 'participante']
        read_only_fields = ['criado_por', 'participante']  # Não permitir que os campos sejam preenchidos na criação

    def create(self, validated_data):
        bolao = Bolao.objects.create(**validated_data)
        return bolao

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        
    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data.get('email')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

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
        fields = ['id', 'team1', 'team2', 'team1_id', 'team2_id', 'final_score1', 'final_score2', 'date']

class BetSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    game = GameSerializer(read_only=True)
    game_id = serializers.PrimaryKeyRelatedField(queryset=Game.objects.all(), write_only=True, source='game')

    class Meta:
        model = Bet
        fields = ['id', 'user', 'game', 'game_id', 'team1_score', 'team2_score', 'created_at']
