from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name = "Home"),
    path('jogador/gerenciar', views.player_manage, name = "player_manage"),
    path('jogador/cadastrar', views.player_register, name = "player_register"),
    path('jogador/editar', views.player_edit, name = "player_edit"),
    path('time/gerenciar', views.team_manage, name = "team_manage"),
    path('time/cadastrar', views.team_register, name = "team_register"),
    path('time/editar', views.team_edit, name = "team_edit"),
    path('jogo', views.game, name = "game"),
    path('esportes', views.sport, name = "sport"),
]