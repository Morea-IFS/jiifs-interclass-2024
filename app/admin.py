from django.contrib import admin
from . models import Volley_match, Player, Assistance, Penalties, Time_pause, Team, Sport, Point, Team_sport, Player_team_sport, Match, Team_match, Player_match

# Register your models here.

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('id','name','sexo')
    search_fields = ('id','name','sexo')

@admin.register(Volley_match)
class Volley_matchAdmin(admin.ModelAdmin):
    list_display = ('id','status','sets_team_a','sets_team_b')
    search_fields = ('id','status','sets_team_a','sets_team_b')

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
    list_display = ('id','sexo','sport','time_match','status','Winner_team','time_start','time_end')
    search_fields = ('id','sexo','sport','time_match','status','Winner_team','time_start','time_end')

@admin.register(Player_match)
class Player_matchAdmin(admin.ModelAdmin):
    list_display = ('id','match','player_number','player')
    search_fields = ('id','match','player_number','player')

@admin.register(Team_match)
class Team_matchAdmin(admin.ModelAdmin):
    list_display = ('id','team','match')
    search_fields = ('id','team','match')

@admin.register(Player_team_sport)
class Team_sportAdmin(admin.ModelAdmin):
    list_display = ('id','player','team_sport')
    search_fields = ('id','player','team_sport')

@admin.register(Point)
class PointAdmin(admin.ModelAdmin):
    list_display = ('id','point_types','player','team_match','time')
    search_fields = ('id','point_types','player','team_match','time')

@admin.register(Penalties)
class PenaltiesAdmin(admin.ModelAdmin):
    list_display = ('id','type_penalties','player','team_match','time')
    search_fields = ('id','type_penalties','player','team_match','time')

@admin.register(Time_pause)
class Time_pauseAdmin(admin.ModelAdmin):
    list_display = ('id','start_pause','end_pause','match')
    search_fields = ('id','start_pause','end_pause','match')

@admin.register(Assistance)
class AssistanceAdmin(admin.ModelAdmin):
    list_display = ('id','assis_to','player','match')
    search_fields = ('id','assis_to','player','match')
