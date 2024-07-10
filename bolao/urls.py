from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import *

urlpatterns = [
    path('campeonatos/', CampeonatoList.as_view(), name='campeonato-list'),
    path('campeonatos/<int:pk>/', CampeonatoDetail.as_view(), name='campeonato-detail'),
    path('boloes/', BolaoList.as_view(), name='bolao-list'),
    path('boloes/<int:pk>/', BolaoDetail.as_view(), name='bolao-detail'),
    path('boloes/myBoloes/', MyBoloesList.as_view(), name='my-boloes-list'),
    path('boloes/<int:bolao_pk>/add-participant/<int:user_pk>/', add_participant, name='add-participant'),
    path('users/', UserList.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetail.as_view(), name='user-detail'),
    path('teams/', TeamList.as_view(), name='team-list'),
    path('teams/<int:pk>/', TeamDetail.as_view(), name='team-detail'),
    path('games/', GameList.as_view(), name='game-list'),
    path('games/<int:pk>/', GameDetail.as_view(), name='game-detail'),
    path('bets/', BetList.as_view(), name='bet-list'),
    path('bets/<int:pk>/', BetDetail.as_view(), name='bet-detail'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]