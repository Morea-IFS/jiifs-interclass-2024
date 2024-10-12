from django.shortcuts import render, redirect, get_object_or_404
from django.utils.dateparse import parse_datetime
from django.http import JsonResponse, HttpResponse
from .models import Sexo, Player, Team, Sport, Team_sport, Player_team_sport, Match, Player_match, Team_match

# Create your views here.
def index(request):
    return render(request, 'index.html')

def player_manage(request):
    player = Player.objects.all()
    return render(request, 'gerenciamento-jogadores.html', {'player': player,})

def player_register(request):
    if request.method == 'GET':
        return render(request, 'cadastro-jogadores.html')
    else:
        name = request.POST.get('name')
        instagram = request.POST.get('instagram')
        sexo = request.POST.get('sexo')
        photo = request.FILES.get('photo')
        number = request.POST.get('number')
        player = Player.objects.create(name=name, instagram=instagram, sexo=sexo, photo=photo, number=number)
        player.save()
        return redirect('player_register')

def player_edit(request, id):
    player = get_object_or_404(Player, id=id)
    if request.method == 'GET':
        return render(request, 'editar-jogadores.html', {'player': player})
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
        player.number = request.POST.get('number')
        player.save()
        return redirect('player_manage')    

def team_manage(request):
    team = Team.objects.all()
    team_sports = Team_sport.objects.select_related('team', 'sport').all()
    
    return render(request, 'gerenciamento-times.html', {'team_sports': team_sports})

def team_register(request):
    sport = Sport.objects.all()
    if request.method == 'GET':
        return render(request, 'cadastro-times.html', {'sport': sport,})
    else:
        name = request.POST.get('name')
        hexcolor = request.POST.get('hexcolor')
        sexo = request.POST.get('sexo')
        photo = request.FILES.get('photo')
        list_sport = request.POST.getlist('sports')
        team = Team.objects.create(name=name, hexcolor=hexcolor, photo=photo)
        team.save()
        for i in list_sport:
            sport_name = Sport.objects.get(id=i)
            Team_sport.objects.create(team=team, sport=sport_name)
        return redirect('team_register')

def team_edit(request, id):
    team = get_object_or_404(Team, id=id)
    sport = Sport.objects.all()
    sport_ids = Team_sport.objects.filter(team=team).values_list('sport_id', flat=True)
    if request.method == 'GET': 
        return render(request, 'editar-times.html', { 'team': team, 'sport': sport, 'sport_ids': sport_ids })
    elif 'excluir' in request.POST:
        if team.photo:
            team.photo.delete()
        Team_sport.objects.filter(team=team).delete()
        team.delete()
        return redirect('team_manage')
    else:
        team.name = request.POST.get('name')
        if team.photo:
            team.photo.delete()
        team.photo = request.FILES.get('photo')
        list_sport = request.POST.getlist('sports')
        team.hexcolor = request.POST.get('hexcolor')
        Team_sport.objects.filter(team=team).delete()
        team.save()
        for i in list_sport:
            sport_name = Sport.objects.get(id=i)
            Team_sport.objects.create(team=team, sport=sport_name)
        return redirect('team_manage')  

def team_players_manage(request, id):
    team = get_object_or_404(Team_sport, id=id)
    if request.method == "GET":
        player_team_sport = Player_team_sport.objects.select_related('player', 'team_sport').filter(team_sport=id)
        return render(request, 'gerenciamento-jogadores-times.html', {'player_team_sport': player_team_sport,'team': team})
    else:
        player = request.POST.getlist('input-checkbox')
        player_sport = Player_team_sport.objects.filter(team_sport=id)
        for i in player:
            player_filter = player_sport.filter(player=i)
            player_filter.delete()
        return redirect('team_players_manage', id=team.id)

def add_player_team(request, id):
    team = get_object_or_404(Team_sport, id=id)
    players = Player.objects.all()
    if request.method == 'GET':
        return render(request, 'adicionar-jogadores-time.html', {'players': players,'team': team}) 
    else:
        player = request.POST.getlist('select')
        print(player)
        for i in player:
            player = Player.objects.get(id=i)
            Player_team_sport.objects.create(player=player, team_sport=team)
        return redirect('team_players_manage', id=team.id)

def matches_manage(request):
    return render(request, 'gerenciamento-partidas.html')

def matches_edit(request):
    return render(request, 'editar-partidas.html')

def matches_register(request):
    return render(request, 'cadastro-partidas.html')

    
def game(request):
    return render(request, 'jogo.html')

def sport(request):
    return render(request, 'esportes.html')
