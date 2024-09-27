from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class Status(models.Model):
    Shortly = 0, "Shortly"
    Happening = 1, "Happening"
    Finished = 2, "Finished"
    Cancelado = 3, "Canceled"
    Paused = 4, "Paused"

    __empty__ = ("Vazio")

class Point_types(models.Model):
    Goal = 0, "Goal"
    Point = 1, "Point"
    Ace = 2, "Ace"

    __empty__ = ("Vazio")

class Activity(models.Model):
    Titular = 0, "Titular"
    Reserva = 1, "Reserva"

    __empty__ = ("Vazio")

class Type_penalties(models.Model):
    cartao_vermelho = 0, "Cartão Vermelho"
    cartao_amarelo = 1, "Cartão Amarelo"

    __empty__ = ("Vazio")

class Sexo(models.Model):
    Masculino = 0, "Masculino"
    Feminino = 1, "Feminino"

    __empty__ = ("Vazio")

class Player(models.Model):
    name = models.CharField(max_length=100)
    instagram = models.CharField(max_length=100, blank=True)
    photo = models.ImageField(upload_to='photo_player/', default='defaults/profile_default.png', blank=True)
    sexo = models.ForeignKey(Sexo, on_delete=models.CASCADE)
    number = models.IntegerField(blank=True, null=True)

    def __str__(self):    
        return f"{self.name} | {self.sexo}"

class Team(models.Model):
    name = models.CharField(max_length=100, blank=True)
    photo = models.ImageField(upload_to='logo_team/', default='defaults/team_default.png', blank=True)
    hexcolor = models.CharField(max_length=6, null=True)

    def __str__(self):    
        return f"{self.name} | {self.hexcolor}"

class Sport(models.Model):
    name = models.CharField(max_length=50)
    max_titulares = models.IntegerField(validators=[MaxValueValidator(50)])

    def __str__(self):    
        return f"{self.name} | {self.max_titulares}"

class Team_sport(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE)

    def __str__(self):    
        return f"{self.team} | {self.sport}"

class Team_match(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    match = models.ForeignKey('Match', on_delete=models.CASCADE)  # Referencia por string

    def __str__(self):    
        return f"{self.team} | {self.match}"

class Volley_match(models.Model):
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    team_match = models.ForeignKey(Team_match, on_delete=models.CASCADE)
    sets_team = models.IntegerField(default=0)

    def __str__(self):    
        return f"{self.status} | {self.team_match} | {self.sets_team}"

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
    horario_pertida = models.TimeField(default=0)

    def __str__(self):    
        return f"{self.id} | {self.sport} | {self.status} | {self.sexo}"

class Point(models.Model):
    type = models.ForeignKey(Point_types, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    team_match = models.ForeignKey(Team_match, on_delete=models.CASCADE)
    time = models.TimeField()

    def __str__(self):    
        return f"{self.type} | {self.player} | {self.team_match} | {self.time}"

class Assistance(models.Model):
    assis_to = models.ForeignKey(Point, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)

    def __str__(self):    
        return f"{self.assis_to} | {self.player}"

class Player_match(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    player_number = models.IntegerField(blank=True, null=True)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)

    def __str__(self):    
        return f"{self.player} | {self.match} | {self.player_number} | {self.activity}"

class Penalties(models.Model):
    type = models.CharField(max_length=100)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    team_match = models.ForeignKey(Team_match, on_delete=models.CASCADE)
    time = models.TimeField()

    def __str__(self):    
        return f"{self.type} | {self.player} | {self.team_match} | {self.time}"

class time_pause(models.Model):
    start_pause = models.TimeField()
    end_pause = models.TimeField()
    match = models.ForeignKey(Match, on_delete=models.CASCADE)

    def __str__(self):    
        if self.start_pause:
            return f"{self.start_pause} | {self.match}"
        elif self.start_pause and self.end_pause:
            return f"{self.start_pause} | {self.end_pause} | {self.match}"