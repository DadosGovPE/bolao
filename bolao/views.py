from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.models import User
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Team, Game, Bet
from .serializers import *

class CampeonatoList(generics.ListCreateAPIView):
    queryset = Campeonato.objects.all()
    serializer_class = CampeonatoSerializer
    permission_classes = [permissions.AllowAny]

class CampeonatoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Campeonato.objects.all()
    serializer_class = CampeonatoSerializer
    permission_classes = [permissions.AllowAny]

class BolaoList(generics.ListCreateAPIView):
    queryset = Bolao.objects.all()
    serializer_class = BolaoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        campeonato = self.request.data.get('campeonato')
        bolao = serializer.save(criado_por=self.request.user, campeonato_id=campeonato)
        bolao.participante.set([self.request.user])  # Adicionar o usuário autenticado como participante

class BolaoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bolao.objects.all()
    serializer_class = BolaoSerializer
    permission_classes = [permissions.AllowAny]

class MyBoloesList(generics.ListAPIView):
    serializer_class = BolaoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Bolao.objects.filter(participante=user)

class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

class TeamList(generics.ListCreateAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class TeamDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class GameList(generics.ListCreateAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class GameDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class MyGameList(generics.ListAPIView):
    serializer_class = GameSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        camp_id = self.kwargs.get('camp_id')
        return Game.objects.filter(campeonato__id=camp_id)

class BetList(generics.ListCreateAPIView):
    queryset = Bet.objects.all()
    serializer_class = BetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        game_id = self.request.data.get('game_id')
        bolao_id = self.request.data.get('bolao')
        game = get_object_or_404(Game, id=game_id)
        bolao = get_object_or_404(Bolao, id=bolao_id)
        
        # Verificar se já existe uma aposta para este usuário e este jogo
        existing_bet = Bet.objects.filter(user=user, game=game, bolao=bolao).first()
        
        if existing_bet:
            # Se a aposta existir, atualizar a aposta existente
            existing_bet.team1_score = self.request.data.get('team1_score')
            existing_bet.team2_score = self.request.data.get('team2_score')
            existing_bet.save()
            serializer.instance = existing_bet
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        # Se não existir, criar uma nova aposta
        serializer.save(user=user, game=game, bolao=bolao)


class BetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bet.objects.all()
    serializer_class = BetSerializer
    permission_classes = [permissions.IsAuthenticated]


class MyBetList(generics.ListAPIView):
    serializer_class = BetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        bolao_id = self.kwargs.get('bolao_id')
        return Bet.objects.filter(user=user, bolao__id=bolao_id)

@api_view(['PATCH'])
@permission_classes([permissions.IsAuthenticated])
def add_participant(request, bolao_pk, user_pk):
    try:
        bolao = Bolao.objects.get(pk=bolao_pk)
    except Bolao.DoesNotExist:
        return Response({'error': 'Bolao não encontrado'}, status=status.HTTP_404_NOT_FOUND)
    
    try:
        user = User.objects.get(pk=user_pk)
    except User.DoesNotExist:
        return Response({'error': 'User não encontrado'}, status=status.HTTP_404_NOT_FOUND)

    bolao.participante.add(user)
    return Response({'status': 'Participante adicionado!'})