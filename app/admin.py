from django.contrib import admin
from . models import Player, Team, Sport, Team_sport, Player_team_sport, Match, Player_match

# Register your models here.

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('id','name','number','sexo')
    search_fields = ('id','name','number','sexo')

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('id','name','hexcolor')
    search_fields = ('id','name','hexcolor')

@admin.register(Sport)
class SportAdmin(admin.ModelAdmin):
    list_display = ('id','name','max_titulares')
    search_fields = ('id','name','max_titulares')    

@admin.register(Team_sport)
class Team_sportAdmin(admin.ModelAdmin):
    list_display = ('id','team','sport')
    search_fields = ('id','team','sport')

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):

    list_display = ('id','sexo','sport','time_match')
    search_fields = ('id','sexo','sport','time_match')

@admin.register(Player_match)
class Player_matchAdmin(admin.ModelAdmin):
    list_display = ('id','match','player_number','player')
    search_fields = ('id','match','player_number','player')

@admin.register(Player_team_sport)
class Team_sportAdmin(admin.ModelAdmin):
    list_display = ('id','player','team_sport')
    search_fields = ('id','player','team_sport')