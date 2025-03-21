from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import views

urlpatterns = [
    path('' , views.home_public, name = "home_public"),
    path('placar' , views.scoreboard_public, name="scoreboard_public"),
    path('scoreboard_projector', views.scoreboard_projector, name="scoreboard_projector"),
    path('sobre', views.about_us, name="about_us"),
    path('login' , views.login, name = "login"),
    path('logout', views.sair, name='logout'),
    path('morea', views.index, name = "Home"),
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
    path('general/data/<int:id>', views.general_data, name = "general_data"),
    path('scoreboard', views.scoreboard, name = "scoreboard"),
    path('manage/settings', views.settings_manage, name="settings_manage"),
    path('register/settings', views.settings_register, name="settings_register"),
    path('manage/banner', views.banner_manage, name="banner_manage"),
    path('register/banner', views.banner_register, name="banner_register"),
    path('players_match/<int:id>', views.players_match, name = "players_match"),
    path('players_in_teams/<int:id>', views.players_in_teams, name = "players_in_teams"),
    path('add_players_match/<int:id>', views.add_players_match, name = "add_players_match"),
    path('timer/<int:id>', views.timer_page, name = "timer"),
    path('erro404', views.page_in_erro404)
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)