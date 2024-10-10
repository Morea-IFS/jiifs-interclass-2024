from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index.html')

def player_manage(request):
    return render(request, 'player_manage.html')

def team_manage(request):
    return render(request, 'team_manage.html')

def team_players_manage(request):
    return render(request, 'team_players_manage.html')

def matches_manage(request):
    return render(request, 'matches_manage.html')

def matches_edit(request):
    return render(request, 'matches_edit.html')

def matches_register(request):
    return render(request, 'matches_register.html')

def add_player_team(request):
    return render(request, 'add_player_team.html')

def player_register(request):
    return render(request, 'player_register.html')

def team_register(request):
    return render(request, 'team_register.html')

def player_edit(request):
    return render(request, 'player_edit.html')

def team_edit(request):
    return render(request, 'team_edit.html')

def games(request):
    return render(request, 'games.html')

def sport_manage(request):
    return render(request, 'sport_manage.html')

def sport_edit(request):
    return render(request, 'sport_edit.html')

def sport_register(request):
    return render(request, 'sport_register.html')

def general_data(request):
    return render(request, 'general_data.html')

def scoreboard(request):
    return render(request, 'scoreboard.html')