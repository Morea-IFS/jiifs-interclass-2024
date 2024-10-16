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
    team_sports = Team_sport.objects.select_related('team', 'sport').all()
    return render(request, 'team_manage.html',{'team_sports': team_sports})

def team_players_manage(request, id):
    team = get_object_or_404(Team_sport, id=id)
    if request.method == "GET":
        player_team_sport = Player_team_sport.objects.select_related('player', 'team_sport').filter(team_sport=id)
        return render(request, 'team_players_manage.html', {'player_team_sport': player_team_sport,'team': team})
    else:
        player = request.POST.getlist('input-checkbox')
        player_sport = Player_team_sport.objects.filter(team_sport=id)
        for i in player:
            player_filter = player_sport.filter(player=i)
            player_filter.delete()
        return redirect('team_players_manage', id=team.id)

def matches_manage(request):
    match = Match.objects.all()
    return render(request, 'matches_manage.html', {'match': match,})

def matches_edit(request, id):
    match = get_object_or_404(Match, id=id)
    sport = Sport.objects.all()
    return render(request, 'matches_edit.html', {'match': match, 'sport': sport,})

def matches_register(request):
    team = Team.objects.all()
    sport = Sport.objects.all()
    if request.method ==  "GET":
        return render(request, 'matches_register.html',{'team': team,'sport': sport,})
    else:
        id= request.POST.get('sport')
        sport = get_object_or_404(Sport, id=id)
        sexo = request.POST.get('sexo')
        team_a_id = request.POST.get('time_a')
        team_b_id = request.POST.get('time_b')
        try:
            team_a = Team.objects.get(id=team_a_id)
            team_b = Team.objects.get(id=team_b_id)
        except Team.DoesNotExist:
            return HttpResponse("Um dos times não foi encontrado.", status=404)
        datetime = request.POST.get('datetime')
        match = Match.objects.create(sport=sport, sexo=sexo, time_match=datetime, status=0)
        match.save()
        Team_match.objects.create(match=match, team=team_a)
        Team_match.objects.create(match=match, team=team_b)
        return redirect('matches_manage')

def add_player_team(request, id):
    team = get_object_or_404(Team_sport, id=id)
    players = Player.objects.all()
    if request.method == 'GET':
        return render(request, 'add_players_team.html', {'players': players,'team': team}) 
    else:
        player = request.POST.getlist('select')
        for i in player:
            player = Player.objects.get(id=i)
            Player_team_sport.objects.create(player=player, team_sport=team)
        return redirect('team_players_manage', id=team.id)

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
    sport = Sport.objects.all()
    if request.method == 'GET':
        return render(request, 'team_register.html', {'sport': sport,})
    else:
        name = request.POST.get('name')
        hexcolor = request.POST.get('hexcolor')
        # sexo = request.POST.get('sexo')
        photo = request.FILES.get('photo')
        list_sport = request.POST.getlist('sports')
        team = Team.objects.create(name=name, hexcolor=hexcolor, photo=photo)
        team.save()
        for i in list_sport:
            sport_name = Sport.objects.get(id=i)
            Team_sport.objects.create(team=team, sport=sport_name)
        return redirect('team_register')

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

def team_edit(request, id):
    team = get_object_or_404(Team, id=id)
    sport = Sport.objects.all()
    sport_ids = Team_sport.objects.filter(team=team).values_list('sport_id', flat=True)
    if request.method == 'GET': 
        return render(request, 'team_edit.html', { 'team': team, 'sport': sport, 'sport_ids': sport_ids })
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
        team.save()
        sports_selected = [int(sport_id) for sport_id in list_sport]
        current_sports = Team_sport.objects.filter(team=team).values_list('sport_id', flat=True)

        to_add = set(sports_selected) - set(current_sports)
        to_remove = set(current_sports) - set(sports_selected)

        for sport_id in to_add:
            sport = get_object_or_404(Sport, id=sport_id)
            Team_sport.objects.create(team=team, sport=sport)

        for sport_id in to_remove:
            Team_sport.objects.filter(team=team, sport_id=sport_id).delete()
    return redirect('team_manage') 

def games(request):
    return render(request, 'games.html')

def sport_manage(request):
    sport = Sport.objects.all()
    return render(request, 'sport_manage.html',{'sport': sport,})

def sport_edit(request, id):
    sport = get_object_or_404(Sport, id=id)
    if request.method == "GET":
        return render(request, 'sport_edit.html', {'sport': sport,})
    elif 'excluir' in request.POST:
        sport.delete()
        return redirect('sport_manage')
    else:
        sport.name = request.POST.get('name')
        sport.max_titulares = request.POST.get('max_titulares')
        sport.save()
        return redirect('sport_manage')

def sport_register(request):
    if request.method =="GET":
        return render(request, 'sport_register.html')
    else:
        name = request.POST.get('name')
        max_titulares = request.POST.get('max_titulares')
        Sport.objects.create(name=name, max_titulares=max_titulares)
        return redirect('sport_register')
    
def general_data(request):
    return render(request, 'general_data.html')

def scoreboard(request):
    return render(request, 'scoreboard.html')

def players_team(request):
    return render(request, 'players_team.html')

def timer(request):
    return render(request, 'timer.html')