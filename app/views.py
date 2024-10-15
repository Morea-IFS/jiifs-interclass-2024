from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from .models import Sexo, Player, Team, Sport, Team_sport, Player_team_sport, Match, Player_match, Team_match

# Create your views here.
def index(request):
    return render(request, 'index.html')

def player_manage(request):
    player = Player.objects.all()
    return render(request, 'player_manage.html', {'player': player})

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
    if request.method == 'GET':
        return render(request, 'player_register.html')
    else:
        name = request.POST.get('name')
        instagram = request.POST.get('instagram')
        sexo = request.POST.get('sexo')
        photo = request.FILES.get('photo')
        player = Player.objects.create(name=name, instagram=instagram, sexo=sexo, photo=photo)
        player.save()
        return redirect('player_register')

def team_register(request):
    return render(request, 'team_register.html')

def player_edit(request):
    return render(request, 'player_edit.html')

def player_edit(request, id):
    player = get_object_or_404(Player, id=id)
    if request.method == 'GET':
        return render(request, 'player_edit.html', {'player': player})
    elif 'excluir' in request.POST:
        if player.photo:
            player.photo.delete()
        player.delete()
        return redirect('player_manage')
    else:
        player.name = request.POST.get('name')
        player.instagram = request.POST.get('instagram')
        player.sexo = request.POST.get('sexo')
        if player.photo:
            player.photo.delete()
            player.photo = request.FILES.get('photo')
        player.save()
        return redirect('player_manage')

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