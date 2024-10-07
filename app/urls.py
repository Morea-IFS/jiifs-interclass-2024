from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name = "Home"),
    path('gerenciar/jogador', views.player_manage, name = "player_manage"),
    path('cadastrar/jogador', views.player_register, name = "player_register"),
    path('editar/jogador', views.player_edit, name = "player_edit"),
    path('gerenciar/time', views.team_manage, name = "team_manage"),
    path('cadastrar/time', views.team_register, name = "team_register"),
    path('editar/time', views.team_edit, name = "team_edit"),
    path('gerenciar/jogadores/time', views.team_players_manage, name = "team_players_manage"),
    path('gerenciar/partidas', views.matches_manage, name = "matches_manage"),
    path('editar/partidas', views.matches_edit, name = "matches_edit"),
    path('adicionar/jogador/time', views.add_player_team, name = "add_player_team"),
    path('cadastrar/partidas', views.matches_register, name = "matches_register"),
    path('jogo', views.game, name = "game"),
    path('gerenciar/esporte', views.sport_manage, name = "sport_manage"),
    path('cadastrar/esporte', views.sport_register, name = "sport_register"),
    path('editar/esporte', views.sport_edit, name = "sport_edit"),
]