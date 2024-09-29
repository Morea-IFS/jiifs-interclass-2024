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
    path('gerenciar/jogadores/time', views.manage_team_players, name = "manage_team_players"),
    path('jogo', views.game, name = "game"),
    path('esportes', views.sport, name = "sport"),
]