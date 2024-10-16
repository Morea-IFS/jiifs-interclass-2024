from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name = "Home"),
    path('manage/player', views.player_manage, name = "player_manage"),
    path('register/player', views.player_register, name = "player_register"),
    path('edit/player/<int:id>', views.player_edit, name = "player_edit"),
    path('manage/team', views.team_manage, name = "team_manage"),
    path('register/team', views.team_register, name = "team_register"),
    path('edit/team/<int:id>', views.team_edit, name = "team_edit"),
    path('manage/player/team/<int:id>', views.team_players_manage, name = "team_players_manage"),
    path('manage/match', views.matches_manage, name = "matches_manage"),
    path('edit/match/<int:id>', views.matches_edit, name = "matches_edit"),
    path('add/player/team/<int:id>', views.add_player_team, name = "add_player_team"),
    path('register/match', views.matches_register, name = "matches_register"),
    path('games', views.games, name = "games"),
    path('manage/sport', views.sport_manage, name = "sport_manage"),
    path('register/sport', views.sport_register, name = "sport_register"),
    path('edit/sport/<int:id>', views.sport_edit, name = "sport_edit"),
    path('general/data', views.general_data, name = "general_data"),
    path('scoreboard/', views.scoreboard, name = "scoreboard"),
    path('players_team', views.players_team, name = "players_team"),
    path('timer', views.timer, name = "timer"),
]