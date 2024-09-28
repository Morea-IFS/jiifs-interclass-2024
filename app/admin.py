from django.contrib import admin
from . models import Player, Team, Sport

# Register your models here.

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('name','number','sexo')
    search_fields = ('name','number','sexo')

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name','hexcolor')
    search_fields = ('name','hexcolor')

@admin.register(Sport)
class SportAdmin(admin.ModelAdmin):
    list_display = ('name','max_titulares')
    search_fields = ('name','max_titulares')    