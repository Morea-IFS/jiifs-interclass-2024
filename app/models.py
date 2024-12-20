from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class Status(models.IntegerChoices):
    shortly = 0, "Em breve"
    happening = 1, "Acontecendo"
    finished = 2, "Finalizada"
    cancelado = 3, "Cancelada"
    paused = 4, "Pausada"
    empty = 5, "Nenhum"

class Point_types(models.IntegerChoices):
    goal = 0, "Gol"
    point = 1, "Ponto"
    ace = 2, "Ace"
    empty = 3, "Nenhum"

class Activity(models.IntegerChoices):
    holder = 0, "Titular"
    reserve = 1, "Reserva"
    empty = 2, "Nenhum"

class Type_penalties(models.IntegerChoices):
    card_red = 0, "Cartão Vermelho"
    card_yellow = 1, "Cartão Amarelo"
    lack = 2, "lack"
    empty = 3, "Nenhum"

class Sexo(models.IntegerChoices):
    masculine = 0, "Masculino"
    feminine = 1, "Feminino"
    empty = 2, "Nenhum"

class Type_Banner(models.IntegerChoices):
    In_use = 0, "Em uso"
    empty = 1, "Nenhum"

class Player(models.Model):
    name = models.CharField(max_length=100)
    instagram = models.CharField(max_length=100, blank=True)
    photo = models.ImageField(upload_to='photo_player/', default='defaults/person.png', blank=True)
    sexo = models.IntegerField(choices=Sexo.choices, default=Sexo.empty)

    def __str__(self):    
        return f"{self.name} | {self.sexo}"

class Team(models.Model):
    name = models.CharField(max_length=100, blank=True)
    photo = models.ImageField(upload_to='logo_team/', default='defaults/team.png', blank=True)
    hexcolor = models.CharField(max_length=7, null=True)

    def __str__(self):    
        return f"{self.name}"

class Sport(models.Model):
    name = models.CharField(max_length=50)
    max_titulares = models.IntegerField(validators=[MaxValueValidator(50)])
    sets = models.BooleanField(default=False, null=True, blank=True)
    logs = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):    
        return f"{self.name}"

class Team_sport(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE)

    def __str__(self):    
        return f"{self.team} | {self.sport}"
    
class Player_team_sport(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    team_sport = models.ForeignKey(Team_sport, on_delete=models.CASCADE)

    def __str__(self):    
        return f"{self.player} | {self.team_sport}"

class Team_match(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    match = models.ForeignKey('Match', on_delete=models.CASCADE, related_name='teams')

    def __str__(self):    
        return f"{self.team} | {self.match}"

class Volley_match(models.Model):
    status = models.IntegerField(choices=Status.choices, default=Status.empty)
    sets_team_a = models.IntegerField(default=0)
    sets_team_b = models.IntegerField(default=0)

    def __str__(self):    
        return f"{self.status} | {self.sets_team_a} | {self.sets_team_b}"

class Match(models.Model):
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE)
    status = models.IntegerField(choices=Status.choices, default=Status.shortly)
    time_start = models.TimeField(blank=True, null=True)
    time_end = models.TimeField(blank=True, null=True)
    sexo = models.IntegerField(choices=Sexo.choices, default=Sexo.empty, blank=True)
    mvp_player_player = models.ForeignKey(Player, on_delete=models.CASCADE, blank=True, null=True)
    Winner_team = models.ForeignKey(Team, on_delete=models.CASCADE, blank=True, null=True)
    volley_match = models.ForeignKey(Volley_match, on_delete=models.CASCADE, blank=True, null=True, related_name="matches")
    add = models.TimeField(blank=True, null=True)
    time_match = models.DateTimeField(null=True, blank=True)

    def __str__(self):    
        return f"{self.id} | {self.sport} | {self.status} | {self.sexo}"

class Point(models.Model):
    point_types = models.IntegerField(choices=Point_types.choices, default=Point_types.empty)
    player = models.ForeignKey(Player, on_delete=models.CASCADE, null=True, blank=True)
    team_match = models.ForeignKey(Team_match, on_delete=models.CASCADE)
    time = models.TimeField(auto_now_add=True)

    def __str__(self):    
        if self.player:
            return f"{self.point_types} | {self.player} | {self.team_match} | {self.time}"
        else:
            return f"{self.point_types} | {self.team_match} | {self.time}"

class Assistance(models.Model):
    assis_to = models.ForeignKey(Point, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE, null=True)

    def __str__(self):    
        return f"{self.assis_to} | {self.player}"

class Player_match(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    player_number = models.IntegerField(blank=True, null=True, default=0)
    activity = models.IntegerField(choices=Activity.choices, default=Activity.empty)
    team_match = models.ForeignKey(Team_match, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):    
        return f"{self.player} | {self.match} | {self.player_number} | {self.team_match} | {self.activity}" 

class Penalties(models.Model):
    type_penalties = models.IntegerField(choices=Type_penalties.choices, default=Type_penalties.empty)
    player = models.ForeignKey(Player, on_delete=models.CASCADE, null=True, blank=True)
    team_match = models.ForeignKey(Team_match, on_delete=models.CASCADE)
    time = models.TimeField(auto_now_add=True)

    def __str__(self):    
        return f"{self.type_penalties} | {self.player} | {self.team_match} | {self.time}"

class Time_pause(models.Model):
    start_pause = models.TimeField()
    end_pause = models.TimeField(null=True, blank=True)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)

    def __str__(self):    
        if self.start_pause:
            return f"{self.start_pause} | {self.match}"
        elif self.start_pause and self.end_pause:
            return f"{self.start_pause} | {self.end_pause} | {self.match}"

class Events(models.Model):
    name = models.CharField(max_length=50)
    details = models.CharField(max_length=200)
    match = models.ForeignKey(Match, on_delete=models.CASCADE, null=True)
    datetime = models.TimeField(auto_now_add=True)
    def __str__(self):    
        return f"{self.name} | {self.details} | {self.details} | {self.datetime}"
    
class Config(models.Model):
    site = models.CharField(max_length=200,null=True, blank=True)
    qrcode = models.ImageField(upload_to='photos_config/', default='defaults/qrcode.png',null=True, blank=True)
    areasup = models.CharField(max_length=50,null=True, blank=True)
    def __str__(self):    
        return f"{self.id} | {self.site}"
    
class Banner(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to='photos_config/', null=True, blank=True)
    status = models.IntegerField(choices=Type_Banner.choices, default=Type_Banner.empty)
    def __str__(self):    
        return f"{self.id} | {self.name} | {self.status}"