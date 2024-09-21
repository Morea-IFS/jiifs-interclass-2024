from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class Status(models.Model):
    Shortly = 0, 'Shortly'
    Happening = 1, 'Happening'
    Finished = 2, 'Finished'
    Cancelado = 3, 'Canceled'
    Paused = 4, 'Paused'

class Point_types(models.Model):
    Goal = 0, 'Goal'
    Point = 1, 'Point'
    Ace = 2, 'Ace'

class Type_penalties(models.Model):
    cartao_vermelho = 0, 'Cartão Vermelho'
    cartao_amarelo = 1, 'Cartão Amarelo'

class Sexo(models.Model):
    Masculino = 0, "Masculino"
    Feminino = 1, "Feminino"

class Player(models.Model):
    name = models.CharField(max_length=100)
    instagram = models.URLField()
    photo = models.ImageField(upload_to='photo_player/', default='defaults/profile_default.png', blank=True)
    sexo = models.CharField(max_lenght=10)

class Team(models.Model):
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='logo_team/', default='defaults/team_default.png', blank=True)
    hexcolor = models.CharField(max_length=7)

class Sport(models.Model):
    name = models.CharField(max_length=50)
    max_titulares = models.IntegerField(validators=[MaxValueValidator(50)])

class Team_sport(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE)

class Team_match(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)

class Volley_match(models.Model):
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    team_match = models.ForeignKey(Team_match, on_delete=models.CASCADE)
    sets_team = models.IntegerField(default=0)

class Match(models.Model):
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    time_start = models.TimeField()
    time_end = models.TimeField()
    sexo = models.ForeignKey(Sexo, on_delete=models.CASCADE)
    mvp_player_player = models.ForeignKey(Player, on_delete=models.CASCADE)
    Winner_team = models.ForeignKey(Team, on_delete=models.CASCADE)
    volley_match = models.ForeignKey(Volley_match, on_delete=models.CASCADE)
    acrescimo = models.TimeField(default=0)

class Point(models.Model):
    type = models.ForeignKey(Point_types, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    team_match = models.ForeignKey(Team_match, on_delete=models.CASCADE)
    Time = models.TimeField()

class Assistance(models.Model):
    assis_to = models.ForeignKey(Point, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)

class Player_match(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    player_number = models.CharField(default="00", max_length=2)

class Penalties(models.Model):
    type = models.CharField(max_length=100)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    team_match = models.ForeignKey(Team_match, on_delete=models.CASCADE)
    time = models.TimeField()

class time_pause(models.Model):
    start_pause = models.TimeField()
    end_pause = models.TimeField()
    match = models.ForeignKey(Match, on_delete=models.CASCADE)


"""
from . models import Match, Sexo, Team_match
"""