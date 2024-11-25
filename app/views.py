from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from .models import Config, Volley_match, Player, Penalties, Events, Time_pause, Team, Sport, Point, Team_sport, Player_team_sport, Match, Team_match, Player_match, Assistance,  Banner
from django.db.models import Count
from django.contrib import messages
from django.db import IntegrityError
from django.templatetags.static import static
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate, logout
from datetime import date
from django.db.models import Prefetch
import time
# Create your views here.
def index(request):
    if request.user.is_authenticated == False:
        return redirect('login')
    else:
        return render (request, 'index.html')
        

def login(request):
    print("kkkkkkkkkkk logado")
    if request.user.is_authenticated == False:
        print("Não está logado")
        if request.method == "GET":
            return render(request, 'login.html')
        else:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user:
                auth_login(request, user)
                return redirect('Home')
            else:
                messages.error(request,"Poxa! alguma informação está incorreta :(")
                return redirect('login')
        print("Está logado")
    else:
        print("kllllllll logado")
        return redirect('Home')
    
def sair(request):
    logout(request)
    return redirect('home_public')

def timer_page(request, id):
    if request.user.is_authenticated == False:
        return redirect('login')
    else:
        match =  Match.objects.get(id=id)
        pauses = Time_pause.objects.filter(match=match)
        context = {
            'match':match,
            'pauses':pauses,
        }
        if request.method == "GET":
            return render(request, 'timer.html', context)
        else:
            pause_id = request.POST.get('pause_delete')
            pause = Time_pause.objects.get(id=pause_id)
            pause.delete()
            return redirect('timer', match.id)

def home_public(request):
    try:
        hoje = date.today()
        games_day = Match.objects.filter(time_match__date=hoje).prefetch_related(
            Prefetch(
                'teams',
                queryset=Team_match.objects.select_related('team'),
                to_attr='prefetched_teams'
            )
        ).select_related('sport').distinct()

        context_games_day = [
            {
                'match': match,
                'sport': match.sport,
                'teams': [
                    {
                        'team': team_match.team,
                        'name': team_match.team.name,
                        'photo_url': team_match.team.photo.url,
                    }
                    for team_match in match.prefetched_teams
                ]
            }
            for match in games_day
        ]


        volei_masc = Volley_match.objects.filter(matches__sexo=0).prefetch_related('matches__teams__team').distinct()
        context_volei_masc = [
            {
                'volley_match': volley_match,
                'sets_team_a': volley_match.sets_team_a,
                'sets_team_b': volley_match.sets_team_b,
                'matches': [
                    {
                        'match': match,
                        'times': [
                            {
                                'team': team_match.team,
                                'name': team_match.team.name,
                                'photo_url': team_match.team.photo.url,
                                'points': Point.objects.filter(team_match=team_match).count()
                            }
                            for team_match in match.teams.all()
                        ]
                    }
                    for match in volley_match.matches.all().order_by('time_match')
                ]
            }
            for volley_match in volei_masc
        ]

        volei_fem = Volley_match.objects.filter(matches__sexo=1).prefetch_related('matches__teams__team').distinct()
        context_volei_fem = [
            {
                'volley_match': volley_match,
                'sets_team_a': volley_match.sets_team_a,
                'sets_team_b': volley_match.sets_team_b,
                'matches': [
                    {
                        'match': match,
                        'times': [
                            {
                                'team': team_match.team,
                                'name': team_match.team.name,
                                'photo_url': team_match.team.photo.url,
                                'points': Point.objects.filter(team_match=team_match).count()
                            }
                            for team_match in match.teams.all()
                        ]
                    }
                    for match in volley_match.matches.all().order_by('time_match')
                ]
            }
            for volley_match in volei_fem
        ]
        
        matchs_futsal_masc = Match.objects.filter(sport__logs=True, sexo=0).prefetch_related('teams__team').order_by('time_match')
        context_futsal_masc = [
            {
                'match': match,
                'times': list(match.teams.all()),
                'points_a': Point.objects.filter(team_match=match.teams.first()).count(),
                'points_b': Point.objects.filter(team_match=match.teams.last()).count(),
            }
            for match in matchs_futsal_masc
        ]

        matchs_futsal_fem = Match.objects.filter(sport__logs=True, sexo=1).prefetch_related('teams__team').order_by('time_match')
        context_futsal_fem = [
            {
                'match': match,
                'times': list(match.teams.all()),
                'points_a': Point.objects.filter(team_match=match.teams.first()).count(),
                'points_b': Point.objects.filter(team_match=match.teams.last()).count(),
            }
            for match in matchs_futsal_fem

        ]

        matchs_queimado_fem = Match.objects.filter(sport__sets=False,sport__logs=False, sexo=0).prefetch_related('teams__team').order_by('time_match')
        context_queimado_fem = [
            {
                'match': match,
                'times': list(match.teams.all()),
                'points_a': Point.objects.filter(team_match=match.teams.first()).count(),
                'points_b': Point.objects.filter(team_match=match.teams.last()).count(),
            }
            for match in matchs_queimado_fem
        ]

        matchs_queimado_masc = Match.objects.filter(sport__sets=False,sport__logs=False, sexo=1).prefetch_related('teams__team').order_by('time_match')
        context_queimado_masc = [
            {
                'match': match,
                'times': list(match.teams.all()),
                'points_a': Point.objects.filter(team_match=match.teams.first()).count(),
                'points_b': Point.objects.filter(team_match=match.teams.last()).count(),
            }
            for match in matchs_queimado_masc
        ]

        if request.method == "GET":
            context = {
                'context_queimado_masc':context_queimado_masc,
                'context_queimado_fem':context_queimado_fem,
                'context_volei_masc':context_volei_masc,
                'context_volei_fem':context_volei_fem,
                'context_futsal_masc':context_futsal_masc,
                'context_futsal_fem':context_futsal_fem,
                'context_games_day':context_games_day,
            }
            print(context)
            return render(request, 'home_public.html', context)
    except Exception as e:
        messages.error(request, f'Um erro inesperado aconteceu: {str(e)}')
        return render(request, 'home_public.html')

def player_manage(request):
    try:
        if request.user.is_authenticated == False:
            return redirect('login')
        else:
            player = Player.objects.all()
            if request.method == "GET":
                if not player:
                    print("Não há nenhum jogador cadastrado!")
                return render(request, 'player_manage.html', {'player': player})
            else:
                player_id = request.POST.get('player_delete')
                player_delete = Player.objects.get(id=player_id)
                player_delete.delete()
                return redirect('player_manage')
    except Exception as e:
        messages.error(request, f'Um erro inesperado aconteceu: {str(e)}')
        return render(request, 'player_manage.html')

def team_manage(request):
    try:
        if request.user.is_authenticated == False:
            return redirect('login')
        else:
            teste = Team.objects.all()
            team_sports = Team_sport.objects.select_related('team', 'sport').all()
            if request.method == "GET":
                return render(request, 'team_manage.html', {'team_sports': team_sports, 'teste': teste,})
            else:
                team_sport_id = request.POST.get('team_sport_delete')
                team_sport_delete = Team_sport.objects.get(id=team_sport_id)
                team_sport_delete.delete()
                return redirect('team_manage')
    except Exception as e:
        messages.error(request, f'Um erro inesperado aconteceu: {str(e)}')
        return render(request, 'team_manage.html')

def team_players_manage(request, id):
    try:
        if request.user.is_authenticated == False:
            return redirect('login')
        else:
            team = get_object_or_404(Team_sport, id=id)
            if request.method == "GET":
                player_team_sport = Player_team_sport.objects.select_related('player', 'team_sport').filter(team_sport=id)
                if not player_team_sport: messages.info(request, "Não há nenhum jogador cadastrado!")        
                return render(request, 'team_players_manage.html', {'player_team_sport': player_team_sport,'team': team})
            else:
                player = request.POST.getlist('input-checkbox')
                player_sport = Player_team_sport.objects.filter(team_sport=id)
                for i in player:
                    player_filter = player_sport.filter(player=i)
                    player_filter.delete()
                return redirect('team_players_manage', team.id)
    except Exception as e:
        messages.error(request, f'Um erro inesperado aconteceu: {str(e)}')
        return render(request, 'team_players_manage.html')

def matches_manage(request):
    try:
        if request.user.is_authenticated == False:
            return redirect('login')
        else:
            matchs = Match.objects.all().prefetch_related('teams__team')
            sport = Sport.objects.all()
            context = [
                {
                    'match': match,
                    'sport':sport,
                    'times': list(match.teams.all()),
                }
                for match in matchs
            ]
            if request.method == "GET":
                if not context:
                    print("Não há nenhuma partida cadastrada!")
                return render(request, 'matches_manage.html',{'context': context,})
            else:
                match_id = request.POST.get('match_delete')
                match_delete = Match.objects.get(id=match_id)
                match_delete.delete()
                return redirect('matches_manage')
    except Exception as e:
        messages.error(request, f'Um erro inesperado aconteceu: {str(e)}')
        return render(request, 'matches_manage.html')

def matches_edit(request, id):
    try:
        if request.user.is_authenticated == False:
            return redirect('login')
        else:
            match = get_object_or_404(Match, id=id)
            team_matchs = Team_match.objects.filter(match=match)
            team = Team.objects.all()
            team_match_a = team_matchs[0]
            team_match_b = team_matchs[1]
            match = get_object_or_404(Match, id=id)
            sport = Sport.objects.all()
            if match.sexo != 1 or 0:
                match_disable = True
            else:
                match_disable = False
            context = {
                'match': match, 
                'sport': sport,
                'team': team,
                'team_match_a': team_match_a,
                'team_match_b': team_match_b,
                'match_disable': match_disable,

            }
            if request.method == "GET":
                return render(request, 'matches_edit.html', context)
            else:
                if 'excluir' in request.POST:
                    print("certin")
                    match.delete()
                    team_match_a.delete()
                    team_match_b.delete()
                    return redirect('matches_manage')
                else:
                    sport_select = request.POST.get('sport')
                    sport = get_object_or_404(Sport, id=sport_select)
                    match.sport = sport
                    match.sexo = request.POST.get('sexo')
                    match.time_match = request.POST.get('datatime')
                    team_a = request.POST.get('team_a')
                    team_b = request.POST.get('team_b')
                    team_match_a.team = get_object_or_404(Team, id=team_a)
                    team_match_b.team = get_object_or_404(Team, id=team_b)
                    team_match_a.save()
                    team_match_b.save()
                    match.time_match = request.POST.get('datetime')
                    match.save()
    except (TypeError, ValueError):
        messages.error(request, 'Um valor foi informado incorretamente!')
    except IntegrityError as e:
        messages.error(request, 'Algumas informações não foram preenchidas :(')
    except Team.DoesNotExist:
        messages.error(request, 'Um dos times não foi informado ou é inexistente!')
    except Exception as e:
        messages.error(request, f'Um erro inesperado aconteceu: {str(e)}')
    return redirect('matches_manage')

def matches_register(request):
    if request.user.is_authenticated == False:
        return redirect('login')
    else:
        team = Team.objects.all()
        sport = Sport.objects.all()
        if request.method ==  "GET":
            return render(request, 'matches_register.html',{'team': team,'sport': sport,})
        else:
            try:
                id= request.POST.get('sport')
                sport = get_object_or_404(Sport, id=id)
                sexo = request.POST.get('sexo')
                team_a_id = request.POST.get('time_a')
                team_b_id = request.POST.get('time_b')
                if team_a_id == team_b_id:
                    messages.error(request, "Você não pode criar uma partida com times iguais!")
                    return redirect('matches_register')
                team_a = Team.objects.get(id=team_a_id)
                team_b = Team.objects.get(id=team_b_id)
                datetime = request.POST.get('datetime')
                if sport.sets:
                    volley_match = Volley_match.objects.create(status=0)
                    volley_match.save()
                    print("O esporte tem sets, blz? :)")
                    match = Match.objects.create(sport=sport, sexo=sexo, time_match=datetime, volley_match=volley_match)
                else:    
                    match = Match.objects.create(sport=sport, sexo=sexo, time_match=datetime)  
                match.save()
                Team_match.objects.create(match=match, team=team_a)
                Team_match.objects.create(match=match, team=team_b)
            except (TypeError, ValueError):
                messages.error(request, 'Um valor foi informado incorretamente!')
                return redirect('matches_register')
            except IntegrityError as e:
                messages.error(request, 'Algumas informações não foram preenchidas :(')
                return redirect('matches_register')
            except Team.DoesNotExist:
                messages.error(request, 'Um dos times não foi informado ou é inexistente!')
                return redirect('matches_register')
            except Exception as e:
                messages.error(request, f'Um erro inesperado aconteceu: {str(e)}')
                return redirect('matches_register')
            return redirect('matches_manage')

def add_player_team(request, id):
    if request.user.is_authenticated == False:
        return redirect('login')
    else:
        team = get_object_or_404(Team_sport, id=id)
        players = Player.objects.all()
        if request.method == 'GET':
            if not players: messages.info(request, "Não tem nenhum jogador cadastrado no sistema!")
            return render(request, 'add_players_team.html', {'players': players,'team': team}) 
        else:
            try:
                player = request.POST.getlist('input-checkbox')
                for i in player:
                    player = Player.objects.get(id=i)
                    Player_team_sport.objects.create(player=player, team_sport=team)
            except (TypeError, ValueError):
                messages.error(request, 'Um valor foi informado incorretamente!')
            except IntegrityError as e:
                messages.error(request, 'Algumas informações não foram preenchidas :(')
            except Exception as e:
                messages.error(request, f'Um erro inesperado aconteceu: {str(e)}')
            return redirect('team_players_manage', id=team.id)

def player_register(request):
    if request.user.is_authenticated == False:
        return redirect('login')
    else:
        if request.method == 'GET':
            return render(request, 'player_register.html')
        else:
            try:
                name = request.POST.get('name')
                instagram = request.POST.get('instagram')
                sexo = request.POST.get('sexo')
                if request.FILES.get('photo'):
                    photo = request.FILES.get('photo')
                    player = Player.objects.create(name=name, instagram=instagram, sexo=sexo, photo=photo)
                else:
                    player = Player.objects.create(name=name, instagram=instagram, sexo=sexo)
                player.save()
            except (TypeError, ValueError):
                messages.error(request, 'Um valor foi informado incorretamente!')
            except IntegrityError as e:
                messages.error(request, 'Algumas informações não foram preenchidas :(')
            except Exception as e:
                messages.error(request, f'Um erro inesperado aconteceu: {str(e)}')
            return redirect('player_register')

def team_register(request):
    if request.user.is_authenticated == False:
        return redirect('login')
    else:
        sport = Sport.objects.all()
        if request.method == 'GET':
            return render(request, 'team_register.html', {'sport': sport,})
        else:
            try:
                print(request.POST)
                if not request.POST.getlist('input-checkbox'):
                    messages.error(request, "Você precisa escolher pelo menos um esporte!")
                    return redirect('team_register')
                name = request.POST.get('name')
                hexcolor = request.POST.get('hexcolor')
                list_sport = request.POST.getlist('input-checkbox')
                # sexo = request.POST.get('sexo')
                if request.FILES.get('photo'):
                    photo = request.FILES.get('photo')
                    team = Team.objects.create(name=name, hexcolor=hexcolor, photo=photo)
                else:
                    messages.info(request,f"Você não informou uma logo para o time: {name}, então a logo será a padrão do sistema.")
                    team = Team.objects.create(name=name, hexcolor=hexcolor)
                team.save()
                for i in list_sport:
                    sport_name = Sport.objects.get(id=i)
                    Team_sport.objects.create(team=team, sport=sport_name)
            except (TypeError, ValueError):
                messages.error(request, 'Um valor foi informado incorretamente!')
            except IntegrityError as e:
                messages.error(request, 'Algumas informações não foram preenchidas :(')
            except Exception as e:
                messages.error(request, f'Um erro inesperado aconteceu: {str(e)}')
            return redirect('team_register')

def player_edit(request, id):
    if request.user.is_authenticated == False:
        return redirect('login')
    else:
        player = get_object_or_404(Player, id=id)
        if request.method == 'GET':
            if player.sexo != 1 or 0:
                player_disable = True
                return render(request, 'player_edit.html', {'player': player,'player_disable':player_disable})
            else:
                player_disable = False
                return render(request, 'player_edit.html', {'player': player})            
        elif 'excluir' in request.POST:
            if player.photo:
                player.photo.delete()
            player.delete()
            return redirect('player_manage')
        else:
            try:
                player.name = request.POST.get('name')
                player.instagram = request.POST.get('instagram')
                player.sexo = request.POST.get('sexo')
                if request.FILES.get('photo'):
                    if player.photo: player.photo.delete()
                    player.photo = request.FILES.get('photo')
                player.save()
            except (TypeError, ValueError):
                messages.error(request, 'Um valor foi informado incorretamente!')
            except IntegrityError as e:
                messages.error(request, 'Algumas informações não foram preenchidas :(')
            except Exception as e:
                messages.error(request, f'Um erro inesperado aconteceu: {str(e)}')
            return redirect('player_manage')
    
def team_edit(request, id):
    if request.user.is_authenticated == False:
        return redirect('login')
    else:
        team = get_object_or_404(Team, id=id)
        sport = Sport.objects.all()
        sport_ids = Team_sport.objects.filter(team=team).values_list('sport_id', flat=True)
        if request.method == 'GET': 
            return render(request, 'team_edit.html', { 'team': team, 'sport': sport, 'sport_ids': sport_ids })
        elif 'excluir' in request.POST:
            try:
                if team.photo:
                    team.photo.delete()
                Team_sport.objects.filter(team=team).delete()

                team.delete()
                return redirect('team_manage')
            except Exception as e:
                messages.error(request, f'Um erro inesperado aconteceu: {str(e)}')
        else:
            try:
                team.name = request.POST.get('name')
                if request.FILES.get('photo'):
                    if team.photo: team.photo.delete()
                    team.photo = request.FILES.get('photo')
                list_sport = request.POST.getlist('input-checkbox')
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
            except (TypeError, ValueError): messages.error(request, 'Um valor foi informado incorretamente!')
            except IntegrityError as e: messages.error(request, 'Algumas informações não foram preenchidas :(')
            except Exception as e: messages.error(request, f'Um erro inesperado aconteceu: {str(e)}')
        return redirect('team_manage') 

def games(request):
    if request.user.is_authenticated == False:
        return redirect('login')
    else:
        matchs = Match.objects.all().prefetch_related('teams__team').order_by('time_match')
        context = [
            {
                'match': match,
                'times': list(match.teams.all()),
                'points_a': Point.objects.filter(team_match=match.teams.first()).count(),
                'points_b': Point.objects.filter(team_match=match.teams.last()).count(),
            }
            for match in matchs
        ]
        return render(request, 'games.html',{'context': context})

def sport_manage(request):
    if request.user.is_authenticated == False:
        return redirect('login')
    else:
        sport = Sport.objects.all()
        if request.method == "GET":
            if not sport:
                print("Não há nenhum time cadastrado!")
            return render(request, 'sport_manage.html',{'sport': sport,})
        else:
            sport_id = request.POST.get('sport_delete')
            sport_delete = Sport.objects.get(id=sport_id)
            sport_delete.delete()
            return redirect('sport_manage')

def sport_edit(request, id):
    if request.user.is_authenticated == False:
        return redirect('login')
    else:
        sport = get_object_or_404(Sport, id=id)
        if request.method == "GET":
            return render(request, 'sport_edit.html', {'sport': sport,})
        elif 'excluir' in request.POST:
            sport.delete()
            return redirect('sport_manage')
        else:
            try:
                if request.POST.get('sets') and request.POST.get('logs') == 'True':
                    messages.error(request, "Erro, o esporte está recebendo sets e logs como verdadeiros, você está informar somente um como verdadeiro.")
                    return redirect('sport_edit', sport.id)
                elif sport.sets == 'True' and sport.logs == 'True':
                    messages.error(request, "o  esporte está recebendo sets e logs como verdadeiros, você está informar somente um como verdadeiro.")
                    return redirect('sport_edit', sport.id) 
                sport.name = request.POST.get('name')
                sport.max_titulares = request.POST.get('max_titulares')
                if request.POST.get('sets') == 'True' or 'False':
                    sport.sets = request.POST.get('sets')
                    sport.save()
                if request.POST.get('logs') == 'True' or 'False':
                    sport.logs = request.POST.get('logs')
                    sport.save()
            except (TypeError, ValueError):
                messages.error(request, 'Um valor foi informado incorretamente!')
                return redirect('sport_edit', sport.id)
            except IntegrityError as e:
                messages.error(request, 'Algumas informações não foram preenchidas :(')
                return redirect('sport_edit', sport.id)
            except Exception as e:
                messages.error(request, f'Um erro inesperado aconteceu: {str(e)}')
                return redirect('sport_edit', sport.id)
            return redirect('sport_manage')

def sport_register(request):
    if request.user.is_authenticated == False:
        return redirect('login')
    else:
        if request.method =="GET":
            return render(request, 'sport_register.html')
        else:
            try:
                name = request.POST.get('name')
                max_titulares = request.POST.get('max_titulares')
                if request.POST.get('sets') != 'False':
                    sets = request.POST.get('sets')
                    Sport.objects.create(name=name, max_titulares=max_titulares, sets=sets)
                elif request.POST.get('logs') != 'False':
                    logs = request.POST.get('logs')
                    Sport.objects.create(name=name, max_titulares=max_titulares, logs=logs)
                else:
                    Sport.objects.create(name=name, max_titulares=max_titulares)
                
                print(request.POST)
            except (TypeError, ValueError): messages.error(request, 'Um valor foi informado incorretamente!')
            except IntegrityError as e: messages.error(request, 'Algumas informações não foram preenchidas :(')
            except Exception as e: messages.error(request, f'Um erro inesperado aconteceu: {str(e)}')
            return redirect('sport_register')
    
def general_data(request, id):
    if request.user.is_authenticated == False:
        return redirect('login')
    else:
        try:
            match = get_object_or_404(Match, id=id)
            if Team_match.objects.filter(match=match):
                team_matchs = Team_match.objects.filter(match=match)
                if team_matchs[0]: team_match_a = team_matchs[0]
                else:
                    match.status = 3
                    match.save()
                    return redirect('games')
                if team_matchs[1]: team_match_b = team_matchs[1]
                else:
                    match.status = 3
                    match.save()      
                    return redirect('games')
                seconds, status = timer(match)
                oi= seconds // 60
                tchau = seconds % 60
                if oi < 10: time_totally= f'0{oi}:{tchau}'
                elif tchau < 10: time_totally= f'{oi}:0{tchau}'
                elif oi < 10 and oi < 10: time_totally= f'0{oi}:0{tchau}'
                else: time_totally= f'{oi}:{tchau}'
                print("hora: ",time_totally)
                point_a = Point.objects.filter(team_match=team_match_a).count()
                point_b = Point.objects.filter(team_match=team_match_b).count()
                card_yellow_a = Penalties.objects.filter(type_penalties=1,team_match=team_match_a).count()
                card_yellow_b = Penalties.objects.filter(type_penalties=1,team_match=team_match_b).count()
                card_red_a = Penalties.objects.filter(type_penalties=0,team_match=team_match_a).count()
                card_red_b = Penalties.objects.filter(type_penalties=0,team_match=team_match_b).count()
                lack_a = Penalties.objects.filter(type_penalties=2,team_match=team_match_a).count()
                lack_b = Penalties.objects.filter(type_penalties=2,team_match=team_match_b).count()
                if request.method =="GET":
                    context = {
                        'match': match,
                        'point_a': point_a,
                        'point_b': point_b,
                        'card_red_a': card_red_a,
                        'card_red_b': card_red_b,
                        'card_yellow_a': card_yellow_a,
                        'card_yellow_b': card_yellow_b,
                        'lack_a': lack_a,
                        'lack_b': lack_b,
                        'team_match_a': team_matchs[0],
                        'team_match_b': team_matchs[1],
                        
                        'time_totally':time_totally,
                    }
                    print(context)
                    return render(request, 'general_data.html', context)
                else:
                    print(request.POST)
                    if Match.objects.filter(status=1) and request.POST.get('status') == '1':
                        messages.error(request, "Já existe uma partida acontecendo!")
                        return redirect('general_data', match.id)
                    else:
                        match.status = request.POST.get('status')
                        if match.status == '2':
                            if point_a > point_b:
                                match.Winner_team = team_match_a.team
                            elif point_b > point_a:
                                match.Winner_team = team_match_b.team
                            if match.sport.sets:
                                volley_match = Volley_match.objects.get(id=match.volley_match.id)
                                volley_match.status = 2
                                volley_match.save()
                            match.save()
                            return redirect('scoreboard')
                        elif match.status == '1':
                            team_matchs = Team_match.objects.filter(match=match)
                            if team_matchs[0] and team_matchs[1]:
                                if team_matchs[0].team.photo and team_matchs[1].team.photo:
                                    if match.sport.sets:
                                        volley_match = Volley_match.objects.get(id=match.volley_match.id)
                                        print(volley_match)
                                        volley_match.status = 1
                                        volley_match.save()
                                else:
                                    messages.error(request, "Os dados referentes a partida estão incompletos, considere adicionar uma logo ao time(s)")
                            else:
                                messages.error(request, "Os dados referentes partida estão incompletos, algum time está com os dados irregulares!")
                            match.save()
                            return redirect('scoreboard')
                        elif match.status == '0':
                            if match.sport.sets:
                                volley_match = Volley_match.objects.get(id=match.volley_match.id)
                                volley_match.status = 0
                                volley_match.save()
                        match.save()
                        return redirect('games')
        except Team_match.DoesNotExist:
            print("O time não está cadastrado na partida ou foi apagado!")
            messages.error(request, "O time não está cadastrado na partida ou foi apagado, então a partida será cancelada!")
            match.status = 3
            match.save()
            return redirect('games')

def Events_time(name, details):
    match = Match.objects.get(status=1)
    Events.objects.create(name=name,details=details, match=match)

def players_in_teams(request, id):
    if request.user.is_authenticated == False:
        return redirect('login')
    else:
        match = get_object_or_404(Match, id=id)
        team_match = Team_match.objects.filter(match=match)
        team_match_a = team_match[0]
        team_match_b = team_match[1]
        context = {
            'team_match_a':team_match_a,
            'team_match_b':team_match_b,
        }
        return render(request, 'players_in_teams.html', context)

def players_match(request, id):
    if request.user.is_authenticated == False:
        return redirect('login')
    else:
        team_match = get_object_or_404(Team_match, id=id)
        player_match = Player_match.objects.filter(team_match=team_match)
        context = {
            'team_match': team_match,
            'player_match': player_match,
        }
        if request.method == "GET":
            return render(request, 'manage_players_match.html', context)
        else:
            try:
                players = request.POST.getlist('input-checkbox')
                select_action = request.POST.get('select-action')
                if 'select-action' in request.POST:
                    if select_action == 'reserva':
                        for i in players:
                            player = get_object_or_404(Player, id=i)
                            player_match_status = Player_match.objects.get(player=player, team_match=team_match)
                            player_match_status.activity = 1
                            player_match_status.save()
                        return redirect('players_match', team_match.id)
                    if select_action == 'titular':
                        for i in players:
                            player = get_object_or_404(Player, id=i)
                            player_match_status = Player_match.objects.get(player=player, team_match=team_match)
                            player_match_status.activity = 0
                            player_match_status.save()
                        return redirect('players_match', team_match.id)
                    if select_action == 'excluir':
                        for i in players:
                            player = get_object_or_404(Player, id=i)
                            player_match = Player_match.objects.get(player=player, team_match=team_match)
                            player_match.delete()
                        return redirect('players_match', team_match.id)
            except (Player.DoesNotExist,Player_match.DoesNotExist):
                print('O jogador não foi encontrado :(')
            except Exception as e:
                print(f'Um erro inesperado aconteceu: {str(e)}')
            return redirect('players_match', team_match.id)
            

def add_players_match(request, id):
    if request.user.is_authenticated == False:
        return redirect('login')
    else:
        team_match = get_object_or_404(Team_match, id=id)
        players = Player.objects.all()
        context = {
            'players': players,
        }
        if request.method == "GET":
            return render(request, 'add_players_match.html',context)
        else:
            try:
                player_id = request.POST.getlist('input-checkbox')
                print("IDs: ",player_id)
                for i in player_id:
                    number = request.POST.get(f'number_{i}')
                    if int(number) < 1:
                        messages.error(request, "Os números precisam ser maior que 1!")
                        return redirect('add_players_match', id)
                    else:
                        print(request.POST.get(f'number_{i}'))              
                        print("ele ta continuando")
                        player = get_object_or_404(Player, id=i)
                        print(player)
                        player_match = Player_match.objects.create(match=team_match.match, team_match=team_match ,player=player, player_number=number)
                        print(player_match)
                        player_match.save()
                        print(player_match, "salvou")
            except ValueError:
                messages.error(request, "Você precisa informar os jogadores e seus respectivos números corretamente!")
                return redirect('add_players_match', id)

            return redirect('players_match', id)

def settings_manage(request):
    if request.user.is_authenticated == False:
        return redirect('login')
    else:
        config = Config.objects.filter()
        if request.method == "GET":
            return render(request,'settings_manage.html', {'config': config,})
        else:
            try:
                config_id = request.POST.get('config_delete')
                config_delete = Config.objects.get(id=config_id)
                config_delete.delete()
                return redirect('settings_manage')
            except (TypeError, ValueError): messages.error(request, 'Um valor foi informado incorretamente!')
            except IntegrityError as e: messages.error(request, 'Algumas informações não foram preenchidas :(')
            except Exception as e: messages.error(request, f'Um erro inesperado aconteceu: {str(e)}')
            return redirect('settings_manage')

def banner_register(request):
    if request.user.is_authenticated == False:
        return redirect('login')
    else:
        if request.method == "GET":
            return render(request, 'banner_register.html')
        else:
            name = request.POST.get('name')
            image = request.FILES.get('banner')
            if not name or not image:
                messages.eror(request, "Você precisa preencher todas as informações!")
                return redirect('banner_register')
            Banner.objects.create(name=name,image=image)
            return redirect('banner_register')

def banner_manage(request):
    if request.user.is_authenticated == False:
        return redirect('login')
    else:
        banner = Banner.objects.filter()
        if request.method == "GET":
            return render(request, 'banner_manage.html',{'banner': banner})
        else:
            try:
                banner_id = request.POST.get('banner_delete')
                banner_delete = Banner.objects.get(id=banner_id)
                banner_delete.delete()
                return redirect('banner_manage')
            except Exception as e: messages.error(request, f'Um erro inesperado aconteceu: {str(e)}')
            return redirect('banner_manage')
    
def settings_register(request):
    if request.user.is_authenticated == False:
        return redirect('login')
    else:
        if request.method == "GET":
            return render(request,'settings_register.html')
        else:
            try:
                if not Config.objects.filter():
                    site = request.POST.get('site')
                    areasup = request.POST.get('areasup')
                    qrcode = request.FILES.get('qrcode')
                    if not site or not areasup or not qrcode:
                        messages.error(request, 'Algumas informações não foram preenchidas :(')
                        return redirect('settings_register')
                    Config.objects.create(site=site, areasup=areasup, qrcode=qrcode)
                    return redirect('settings_register')
                else:
                    messages.error(request, "Já existe uma configuração vigente, considere apaga-la antes de criar uma nova!")
                    return redirect('settings_manage')
            except (TypeError, ValueError): messages.error(request, 'Um valor foi informado incorretamente!')
            except IntegrityError as e: messages.error(request, 'Algumas informações não foram preenchidas :(')
            except Exception as e: messages.error(request, f'Um erro inesperado aconteceu: {str(e)}')
            return redirect('settings_register')

def scoreboard(request):
    if request.user.is_authenticated == False:
        return redirect('login')
    else:
        try:
            if Match.objects.filter(status=1):
                time_now = time.strftime("%H:%M:%S", time.localtime())
                time_now2 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                match = Match.objects.get(status=1)
                Config.objects.get()
                banner = Banner.objects.all()
                team_matchs = Team_match.objects.filter(match=match)
                team_match_all = Team_match.objects.all()
                players_match = Player_match.objects.filter(match=match)
                team_match_a = team_matchs[0]
                team_match_b = team_matchs[1]
                players_match_a = players_match.filter(team_match=team_match_a)
                players_match_b = players_match.filter(team_match=team_match_b)
                points = Point.objects.filter(team_match=team_match_a).union(
                    Point.objects.filter(team_match=team_match_b)
                ).order_by('time')
                matches = Match.objects.filter(status=0)
                if match.sport.sets:
                    point_a = Point.objects.filter(team_match=team_match_a,point_types=1).count()
                    point_b = Point.objects.filter(team_match=team_match_b,point_types=1).count()
                else:
                    point_a = Point.objects.filter(team_match=team_match_a).count()
                    point_b = Point.objects.filter(team_match=team_match_b).count()
                aces_a = Point.objects.filter(team_match=team_match_a,point_types=2).count()
                aces_b = Point.objects.filter(team_match=team_match_b,point_types=2).count()
                points_a = point_a + aces_a
                points_b = point_b + aces_b
                seconds, status = timer(match)
                context = {
                    'match': match,
                    'banner': banner,
                    'team_match_a':team_match_a,
                    'team_match_b':team_match_b,
                    'team_match_all':team_match_all,
                    'players_match_a':players_match_a,
                    'players_match_b':players_match_b,
                    'team_matchs':team_matchs,
                    'points':points,
                    'point_a':point_a,
                    'point_b':point_b,
                    'aces_a':aces_a,
                    'aces_b':aces_b,
                    'matches':matches,
                    'seconds': seconds,
                    'status': status,
                }
                if request.method == "GET":
                    if match.status == 1:
                        return render(request, 'scoreboard.html', context)
                elif request.method == "POST":
                    try:
                        print("REQUEST: ",request.POST)
                        if 'team_a_sets_add' in request.POST:
                            print("gg")
                            player_select = request.POST.get('player_point')
                            print(player_select)
                            if player_select == "0":
                                Point.objects.create(team_match=team_match_a, point_types=2)
                            else:
                                player = Player.objects.get(id=player_select)
                                Point.objects.create(team_match=team_match_a, point_types=2, player=player)              
                            return redirect('scoreboard')
                        elif 'team_b_sets_add' in request.POST:
                            print("gg")
                            player_select = request.POST.get('player_point')
                            if player_select == "0" :
                                Point.objects.create(team_match=team_match_b, point_types=2)
                            else:
                                player = Player.objects.get(id=player_select)
                                Point.objects.create(team_match=team_match_b, point_types=2, player=player)              
                            return redirect('scoreboard')
                        elif 'team_a_sets_remove' in request.POST:
                            if Point.objects.filter(team_match=team_match_a, point_types=2):
                                point_a_remove = Point.objects.filter(team_match=team_match_a, point_types=2)
                                point_a_remove_last = point_a_remove.last()
                                point_a_remove_last.delete()
                            return redirect('scoreboard')
                        elif 'team_b_sets_remove' in request.POST:
                            if Point.objects.filter(team_match=team_match_b, point_types=2):
                                point_b_remove = Point.objects.filter(team_match=team_match_b, point_types=2)
                                point_b_remove_last = point_b_remove.last()
                                point_b_remove_last.delete()
                            return redirect('scoreboard')
                        if 'team_a_add' in request.POST:
                            player_select = request.POST.get('player_point')
                            print(player_select)
                            if player_select == "0":
                                if match.sport.sets: Point.objects.create(team_match=team_match_a, point_types=1)  
                                else: Point.objects.create(team_match=team_match_a, point_types=0)    
                            else:
                                player = Player.objects.get(id=player_select)
                                if match.sport.sets: Point.objects.create(team_match=team_match_a, point_types=1, player=player)  
                                else: 
                                    point = Point.objects.create(team_match=team_match_a, point_types=0, player=player) 
                                    point.save()  
                                    if match.sport.logs:
                                        Events_time('Gol', f'() {point.player.name} do {team_match_a.team.name} marcou um gol!')                    
                            return redirect('scoreboard')
                        elif 'team_b_add' in request.POST:
                            player_select = request.POST.get('player_point')
                            if player_select == "0" :
                                
                                if match.sport.sets: Point.objects.create(team_match=team_match_b, point_types=1)  
                                else: 
                                    point = Point.objects.create(team_match=team_match_b, point_types=0) 
                                    point.save()  
                                    if match.sport.logs:
                                        Events_time('Gol', f'() {point.player.name} do {team_match_b.team.name} marcou um gol!')
                            else:
                                player = Player.objects.get(id=player_select)
                                if match.sport.sets: Point.objects.create(team_match=team_match_b, point_types=1, player=player)  
                                else: Point.objects.create(team_match=team_match_b, point_types=0, player=player)                                     
                            return redirect('scoreboard')
                        elif 'team_a_remove' in request.POST:
                            if Point.objects.filter(team_match=team_match_a , point_types=0) or Point.objects.filter(team_match=team_match_a , point_types=1):
                                if match.sport.sets: point_a_remove = Point.objects.filter(team_match=team_match_a, point_types=1)
                                else: point_a_remove = Point.objects.filter(team_match=team_match_a, point_types=0)
                                point_a_remove_last = point_a_remove.last()
                                point_a_remove_last.delete()
                            return redirect('scoreboard')
                        elif 'team_b_remove' in request.POST:
                            if Point.objects.filter(team_match=team_match_b , point_types=0) or Point.objects.filter(team_match=team_match_b , point_types=1):
                                if match.sport.sets: point_b_remove = Point.objects.filter(team_match=team_match_b, point_types=1)
                                else: point_b_remove = Point.objects.filter(team_match=team_match_b, point_types=0)
                                point_b_remove_last = point_b_remove.last()
                                point_b_remove_last.delete()
                            return redirect('scoreboard')
                        elif 'type_penalties' in request.POST:
                            type_penalties = request.POST.get('type_penalties')
                            player = get_object_or_404(Player, id=request.POST.get('player_penalties'))
                            print("player: ",player)
                            player_penalties = Player_match.objects.get(player=player, match=match)
                            print("player penalties: ",player_penalties)
                            penalties = Penalties.objects.create(type_penalties=type_penalties, player=player_penalties.player, team_match=player_penalties.team_match)
                            print("chegou ate o evento")
                            penalties.save()
                            print(penalties.get_type_penalties_display(), penalties.type_penalties)
                            print("saiu do evento")
                            if penalties.type_penalties == '0': 
                                penaltie = "Cartão vermelho"
                            elif penalties.type_penalties == '1': 
                                penaltie = "Cartão amarelo"
                            else: 
                                penaltie = "Falta"
                            Events_time(f'{penaltie}', f'{penalties.player.name} do time {penalties.team_match.team.name} recebeu {penaltie.lower()}!')
                            return redirect('scoreboard')
                        elif 'player_winner' in request.POST:
                            player = get_object_or_404(Player, id=request.POST.get('player_winner'))
                            print("player: ",player)
                            match.mvp_player_player = player
                            match.save()
                            return redirect('scoreboard')
                        elif 'databanner' in request.POST and request.POST.get('databanner') != '':
                            banner_id = request.POST.get('databanner')
                            if Banner.objects.filter(status=0).exclude(id=banner_id):
                                banner_geral = Banner.objects.filter(status=0)
                                for i in banner_geral:
                                    i.status = 1
                                    i.save()
                            banner = Banner.objects.get(id=banner_id)
                            if banner.status == 0:
                                banner.status = 1
                                banner.save()
                                messages.info(request, "Imagem de fundo removida!")
                            else:
                                banner.status = 0
                                messages.info(request, "Imagem de fundo adicionada!")
                                banner.save()
                            messages.info(request, "Sucesso!")
                            return redirect('scoreboard')
                        elif 'create_sets' in request.POST:
                            if match.sport.sets:
                                volley_match = Volley_match.objects.get(status=1)
                                sport = get_object_or_404(Sport, id=match.sport.id)
                                match.status = 2
                                match.save()
                                if points_a > points_b:
                                    volley_match.sets_team_a += 1
                                elif points_b > points_a:
                                    volley_match.sets_team_b += 1
                                volley_match.save()
                                print("CRIANDO NOVO SET")
                                print("1:: ",volley_match)
                                new_match = Match.objects.create(sport=sport, sexo=match.sexo, status=5, volley_match=volley_match,time_match=time_now2)
                                print(new_match)
                                new_match.save()
                                team_a_match = Team_match.objects.create(match=new_match, team=team_match_a.team)
                                team_a_match.save()
                                print("2:: ",team_a_match)
                                team_b_match = Team_match.objects.create(match=new_match, team=team_match_b.team)
                                team_b_match.save()
                                print("3:: ",team_b_match)
                                new_match.status = 1
                                new_match.save()
                                for i in players_match_a:
                                    player_match = Player_match.objects.create(match=new_match, team_match=team_a_match ,player=i.player, player_number=i.player_number)
                                    player_match.save()
                                for i in players_match_b:
                                    player_match = Player_match.objects.create(match=new_match, team_match=team_b_match ,player=i.player, player_number=i.player_number)
                                    player_match.save()
                                print("criado com sucesso")
                                return redirect('scoreboard')
                            else:
                                messages.error(request, 'OS SETS SÓ PODEM SER CRIADOS EM ESPORTES QUE NECESSITAM DELE. EX: VOLEIBOL')
                                print("O sets só podem ser criados em esportes que necessitam dele. Ex: Voleibol")
                                return redirect('scoreboard')

                        elif 'finally_start_match' in request.POST:
                            if match.time_start and not match.time_end:
                                messages.error(request, "Antes de finalizar a partida e iniciar outra você precisa primeiro parar o cronometro!")
                                return redirect('scoreboard')
                            print("chegou na primeira parte")
                            next_match_id = request.POST.get('finally_start_match')
                            next_match = Match.objects.get(id=next_match_id)
                            if Volley_match.objects.filter(status=1) or match.sport.sets:
                                print("A partida anterios é de vollei")
                                volley_match = get_object_or_404(Volley_match, status=1)
                                print("volley: ",volley_match)
                                print("mudando estatus da partida")
                                match.status = 2
                                match.save()
                                print("mUdeii:")
                                print(volley_match.status)
                                volley_match.status= 2 
                                volley_match.save()
                                print("Foi finalizada de vez!")
                            else:
                                print("A partida anterios é qualquer uma")
                                match.status = 2
                                match.save()
                                print("Foi finalizada!", match.get_status_display())
                            if next_match.sport.sets:
                                print("A proxima é de vollei tb")
                                volley_match = Volley_match.objects.get(id=next_match.volley_match.id)
                                print(volley_match)
                                print(volley_match.status)
                                volley_match.status = 1
                                volley_match.save()
                            else:
                                print("A proxima é aleatoria")
                            print(next_match, next_match.get_status_display())
                            team_matchs = Team_match.objects.filter(match=next_match)
                            if team_matchs[0] and team_matchs[1]:
                                if team_matchs[0].team.photo and team_matchs[1].team.photo:
                                    next_match.status = 1
                                    next_match.save()
                                    print(next_match)
                                    return redirect('scoreboard')
                                else:
                                    messages.error(request, "Os dados referentes a proxima partida estão incompletos, considere adicionar uma logo ao time(s)")
                            else:
                                messages.error(request, "Os dados referentes a proxima partida estão incompletos, algum time está com os dados irregulares!")
                                next_match.status = 3
                                next_match.save()
                                print(next_match)
                                return redirect('games')
                        elif 'point_assistance' in request.POST:
                            point = get_object_or_404(Point, id=request.POST.get('point_assistance'))
                            player = get_object_or_404(Player, id=request.POST.get('player_assistance'))
                            print(player.name)
                            if point.player == player: messages.error(request, "O mesmo jogador que marcou o ponto foi adicionado como jogador que deu a assistência.")
                            else: 
                                Assistance.objects.create(assis_to=point,player=player, match=match)
                                if point.player.name:
                                    Events_time('Assistência', f'{player.name} deu assistência a {point.player.name} para marcar um {point.get_point_types_display().lower()}!')
                                else:
                                    messages.error(request, 'Não foi possivel registrar essa assistencia, o jogador que marcou o ponto, ace ou gol não foi registrado!')
                            return redirect('scoreboard')
                        
                        elif 'status' in request.POST:
                            print("status")
                            match.status = request.POST.get('status')
                            match.save()
                            if match.status == 1:
                                return redirect('scoreboard')
                            else:
                                return redirect('games')
                        elif 'add_time' in request.POST and request.POST.get('add_time') != '':
                            match.add = request.POST.get('add_time')
                            match.save()
                            return redirect('scoreboard')
                        elif 'time_init' in request.POST:
                            if match.time_start and match.time_end:
                                print("O cronometro já finalizou!")
                                return redirect('scoreboard')
                            
                            elif match.time_start:
                                print("O cronometro já iniciou")
                                return redirect('scoreboard')
                            
                            else:
                                match.time_start = time_now
                                match.save()
                                return redirect('scoreboard')
                                
                        elif 'time_pause' in request.POST:
                            print(request.POST)
                            if match.time_start and match.time_end:
                                print("O cronometro.... finalizado!")
                                return redirect('scoreboard')
                            
                            elif match.time_start:
                                if Time_pause.objects.filter(match=match):
                                    pause = Time_pause.objects.filter(match=match).last()
                                    if pause.start_pause and not pause.end_pause:
                                        pause.end_pause = time_now
                                        pause.save()
                                        return redirect('scoreboard')                
                                    else:
                                        pause_time = Time_pause.objects.create(start_pause=time_now,match=match)
                                        pause_time.save()
                                        return redirect('scoreboard')
                                else:
                                    pause_time = Time_pause.objects.create(start_pause=time_now,match=match)
                                    pause_time.save()
                                    print(pause_time)
                                    return redirect('scoreboard')
                            else:
                                print("Você precisa iniciar o tempo primeiro!")
                                return redirect('scoreboard')
                                
                        elif 'time_stop' in request.POST:
                            if match.time_start and match.time_end:
                                print("O cronometro foi finalizado!")
                                return redirect('scoreboard')
                            elif match.time_start:
                                if Time_pause.objects.filter(match=match).last():
                                    pause = Time_pause.objects.filter(match=match).last()
                                    if pause.start_pause and not pause.end_pause:
                                        pause.end_pause = time_now
                                        pause.save()
                                match.time_end = time_now
                                match.save()
                                return redirect('scoreboard')
                            else:
                                print("o cronometro precisa ser iniciado, para ser finalizado!")
                                return redirect('scoreboard')
                        return redirect('games')
                    except (TypeError, ValueError):
                        messages.error(request, 'Um valor foi informado incorretamente!')
                    except IntegrityError as e:
                        messages.error(request, 'Algumas informações não foram preenchidas :(')
                    except Exception as e:
                        messages.error(request, f'Um erro inesperado aconteceu: {str(e)}')
                    return redirect('scoreboard')
                return redirect('scoreboard')
        except Config.DoesNotExist:
            messages.error(request, "Por favor, adicione as informações do config, elas são importantes para o placar do projetor!")
            return redirect('games')
        return redirect('games')

def scoreboard_public(request):
    try:
        if Volley_match.objects.filter(status=1):
            print("PARTIDA DE VOLEI")
            volley_match = Volley_match.objects.get(status=1)
            print(volley_match)
            match = Match.objects.filter(volley_match=volley_match.id).last()
            print(match)
            team_matchs = Team_match.objects.filter(match=match)
            print(team_matchs)
            team_match_a = team_matchs[0]
            team_match_b = team_matchs[1]
            if (match.volley_match.sets_team_a + match.volley_match.sets_team_b) % 2 == 0:
                print("par")
                teammatch1 = team_match_a
                teammatch2 = team_match_b
                sets_1 = match.volley_match.sets_team_a
                sets_2 = match.volley_match.sets_team_b
            else:
                print("impar")
                teammatch1 = team_match_b
                teammatch2 = team_match_a
                sets_1 = match.volley_match.sets_team_b
                sets_2 = match.volley_match.sets_team_a
            players_match_a = Player_match.objects.filter(team_match=teammatch1)
            players_match_b = Player_match.objects.filter(team_match=teammatch2)
            point_a = Point.objects.filter(team_match=teammatch1).count()
            point_b = Point.objects.filter(team_match=teammatch2).count()
            aces_a = Point.objects.filter(point_types=2,team_match=teammatch1).count()
            aces_b = Point.objects.filter(point_types=2,team_match=teammatch2).count()
            lack_a = Penalties.objects.filter(type_penalties=2,team_match=teammatch1).count()
            lack_b = Penalties.objects.filter(type_penalties=2,team_match=teammatch2).count()
            events = Events.objects.filter(match=match)
            name_scoreboard = 'Sets'
            ball_sport = static('images/ball-of-volley.png')
            if match.sexo == 1: 
                img_sexo = static('images/icon-female.svg')
                sexo_color = '#ff32aa' 
            else: 
                img_sexo = static('images/icon-male.svg')
                sexo_color = '#3a7bd5'
            context = {
                'match': match,
                'team_match_a':teammatch1,
                'team_match_b':teammatch2,
                'time_sets_a': sets_1,
                'sets_b': sets_2,
                'players_match_a':players_match_a,
                'players_match_b':players_match_b,
                'point_a':point_a,
                'point_b':point_b,
                'lack_a':lack_a,
                'lack_b':lack_b,
                'img_sexo':img_sexo,
                'sexo_color': sexo_color,
                'ball_sport': ball_sport,
                'aces_or_card': "Aces",
                'aces_or_card_a': aces_a,
                'aces_or_card_b': aces_b,
                'events': events,
                'sexo_text':match.get_sexo_display(),
                'name_scoreboard': name_scoreboard,
                
            }
            print(context)
            return render(request, 'scoreboard_public.html', context)
            
        elif Match.objects.filter(status=1):
            print("sport aleatorio")
            match = Match.objects.get(status=1)
            events = Events.objects.filter()
            team_matchs = Team_match.objects.filter(match=match)
            team_match_a = team_matchs[0]
            team_match_b = team_matchs[1]
            players_match_a = Player_match.objects.filter(team_match=team_match_a)
            players_match_b = Player_match.objects.filter(team_match=team_match_b)
            point_a = Point.objects.filter(team_match=team_match_a).count()
            point_b = Point.objects.filter(team_match=team_match_b).count()
            lack_a = Penalties.objects.filter(type_penalties=2,team_match=team_match_a).count()
            lack_b = Penalties.objects.filter(type_penalties=2,team_match=team_match_b).count()
            card_a = Penalties.objects.filter(type_penalties=0,team_match=team_match_a).count() + Penalties.objects.filter(type_penalties=1,team_match=team_match_a).count()
            card_b = Penalties.objects.filter(type_penalties=0,team_match=team_match_b).count() + Penalties.objects.filter(type_penalties=1,team_match=team_match_b).count()
            seconds, status = timer(match)
            if match.sexo == 1: 
                img_sexo = static('images/icon-female.svg')
                sexo_color = '#ff32aa' 
            else: 
                img_sexo = static('images/icon-male.svg')
                sexo_color = '#3a7bd5'
            name_scoreboard = 'Tempo'
            ball_sport = static('images/ball-of-futsal.png')
            context = {
                'match': match,
                'events':events,
                'status': status,
                'seconds': seconds,
                'team_match_a':team_match_a,
                'team_match_b':team_match_b,
                'players_match_a':players_match_a,
                'players_match_b':players_match_b,
                'point_a':point_a,
                'point_b':point_b,
                'time_sets_a': "00:00",
                'lack_a':lack_a,
                'lack_b':lack_b,
                'img_sexo':img_sexo,
                'sexo_color': sexo_color,
                'ball_sport': ball_sport,
                'aces_or_card': "Cartões",
                'aces_or_card_a': card_a,
                'aces_or_card_b': card_b,
                'sexo_text':match.get_sexo_display(),
                'name_scoreboard': name_scoreboard,
                
            }
            print(events)
            print(context)
            return render(request, 'scoreboard_public.html', context)
        else:
            return render(request, 'scoreboard_public.html')
    except Exception as e:
        messages.error(request, f'Um erro inesperado aconteceu: {str(e)}')
        return render(request, 'scoreboard_public.html')
def scoreboard_projector(request):
    try:
        if Volley_match.objects.filter(status=1):
            print("PARTIDA DE VOLEI")
            volley_match = Volley_match.objects.get(status=1)
            match = Match.objects.filter(volley_match=volley_match.id).last()
            team_matchs = Team_match.objects.filter(match=match)
            config = Config.objects.get()
            print("config: ",config)
            team_match_a = team_matchs[0]
            team_match_b = team_matchs[1]
            if (match.volley_match.sets_team_a + match.volley_match.sets_team_b) % 2 == 0:
                print("par")
                teammatch1 = team_match_a
                teammatch2 = team_match_b
                sets_1 = match.volley_match.sets_team_a
                sets_2 = match.volley_match.sets_team_b
            else:
                print("impar")
                teammatch1 = team_match_b
                teammatch2 = team_match_a
                sets_1 = match.volley_match.sets_team_b
                sets_2 = match.volley_match.sets_team_a
            if Banner.objects.filter(status=0): 
                banner_score = Banner.objects.get(status=0).image.url
                banner_bol = True
            else: 
                banner_score = static('images/logo-morea.svg')
                banner_bol = False
            players_match_a = Player_match.objects.filter(team_match=teammatch1)
            players_match_b = Player_match.objects.filter(team_match=teammatch2)
            point_a = Point.objects.filter(team_match=teammatch1).count()
            point_b = Point.objects.filter(team_match=teammatch2).count()
            print(point_a, point_b)
            aces_a = Point.objects.filter(point_types=2,team_match=teammatch1).count()
            aces_b = Point.objects.filter(point_types=2,team_match=teammatch2).count()
            lack_a = Penalties.objects.filter(type_penalties=2,team_match=teammatch1).count()
            lack_b = Penalties.objects.filter(type_penalties=2,team_match=teammatch2).count()
            card_a = Penalties.objects.filter(type_penalties=0,team_match=teammatch1).count() + Penalties.objects.filter(type_penalties=1,team_match=teammatch1).count()
            card_b = Penalties.objects.filter(type_penalties=0,team_match=teammatch2).count() + Penalties.objects.filter(type_penalties=1,team_match=teammatch2).count()
            events = Events.objects.filter()
            name_scoreboard = 'Sets'
            ball_sport = static('images/ball-of-volley.png')
            if match.sexo == 1: 
                img_sexo = static('images/icon-female.svg')
                sexo_color = '#ff32aa' 
            else: 
                img_sexo = static('images/icon-male.svg')
                sexo_color = '#3a7bd5'
            context = {
                'match': match,
                'config': config,
                'time_sets_a': sets_1,
                'sets_b': sets_2,
                'team_match_a':teammatch1,
                'team_match_b':teammatch2,
                'players_match_a':players_match_a,
                'players_match_b':players_match_b,
                'point_a':point_a,
                'point_b':point_b,
                'lack_a':lack_a,
                'lack_b':lack_b,
                'img_sexo':img_sexo,
                'sexo_color': sexo_color,
                'ball_sport': ball_sport,
                'aces_a': aces_a,
                'aces_b': aces_b,
                'card_a':card_a,
                'card_b':card_b,
                'events': events,
                'banner_score':banner_score,
                'banner_bol':banner_bol,
                'sexo_text':match.get_sexo_display(),
                'name_scoreboard': name_scoreboard,
                
            }
            print(context)
            return render(request, 'scoreboard_projector.html', context)
            
        elif Match.objects.filter(status=1):
            print("sport aleatorio")
            match = Match.objects.get(status=1)
            events = Events.objects.filter(match=match)
            team_matchs = Team_match.objects.filter(match=match)
            team_match_a = team_matchs[0]
            team_match_b = team_matchs[1]
            config = Config.objects.get()
            print("config: ",config)
            players_match_a = Player_match.objects.filter(team_match=team_match_a)
            players_match_b = Player_match.objects.filter(team_match=team_match_b)
            point_a = Point.objects.filter(team_match=team_match_a).count()
            point_b = Point.objects.filter(team_match=team_match_b).count()
            lack_a = Penalties.objects.filter(type_penalties=2,team_match=team_match_a).count()
            lack_b = Penalties.objects.filter(type_penalties=2,team_match=team_match_b).count()
            card_a = Penalties.objects.filter(type_penalties=0,team_match=team_match_a).count() + Penalties.objects.filter(type_penalties=1,team_match=team_match_a).count()
            card_b = Penalties.objects.filter(type_penalties=0,team_match=team_match_b).count() + Penalties.objects.filter(type_penalties=1,team_match=team_match_b).count()
            seconds, status = timer(match)
            name_scoreboard = 'Tempo'
            ball_sport = static('images/ball-of-futsal.png')
            if Banner.objects.filter(status=0): 
                banner_score = Banner.objects.get(status=0).image.url
                banner_bol = True
            else: 
                banner_score = static('images/logo-morea.svg')
                banner_bol = False
            context = {
                'match': match,
                'events':events,
                'time_sets_a': "00:00",
                'config': config,
                'status': status,
                'seconds': seconds,
                'team_match_a':team_match_a,
                'team_match_b':team_match_b,
                'players_match_a':players_match_a,
                'players_match_b':players_match_b,
                'point_a':point_a,
                'point_b':point_b,
                'lack_a':lack_a,
                'lack_b':lack_b,
                'ball_sport': ball_sport,
                'aces_a': 0,
                'aces_b': 0,
                'banner_score':banner_score,
                'banner_bol':banner_bol,
                'card_a': card_a,
                'card_b': card_b,
                'sexo_text':match.get_sexo_display(),
                'name_scoreboard': name_scoreboard,
                
            }
            print(events)
            print(context)
            return render(request, 'scoreboard_projector.html', context)
        else:
            return render(request, 'scoreboard_projector.html', context)
    except Config.DoesNotExist:
        messages.info(request, "Por favor, adicione as informações do config, ela são importantes para o placar!")
        return render(request, 'scoreboard_projector.html')
    except Exception as e:
        messages.error(request, f'Um erro inesperado aconteceu: {str(e)}')
        return render(request, 'scoreboard_projector.html')
        

    
def timer(match):
    print("kkkkkkkkkk")
    rel = time.localtime()
    match = match
    seconds = 0
    if match.time_start and match.time_end:
        seconds = (match.time_end.hour * 60 * 60 + match.time_end.minute * 60 + match.time_end.second) - (match.time_start.hour * 60 * 60 + match.time_start.minute * 60 + match.time_start.second)
        status = 3
        if Time_pause.objects.filter(match=match):
            pausas_totais = Time_pause.objects.filter(match=match)
            somatorio = 0
            for i in pausas_totais: somatorio += (i.end_pause.hour * 60 * 60 + i.end_pause.minute * 60 + i.end_pause.second) - (i.start_pause.hour * 60 * 60 + i.start_pause.minute * 60 + i.start_pause.second)
            seconds -= somatorio
            print(seconds)
    elif match.time_start:
        print("kk: ",seconds)
        if Time_pause.objects.filter(match=match):
            seconds = (rel.tm_hour * 60 * 60 + rel.tm_min * 60 + rel.tm_sec) - (match.time_start.hour * 60 * 60 + match.time_start.minute * 60 + match.time_start.second)
            pause = Time_pause.objects.filter(match=match).last()
            pausas_totais = Time_pause.objects.filter(match=match)
            somatorio = 0
            if pause.start_pause and pause.end_pause:
                print("Entrou no pausa finalizada jogo continua")
                status = 1
                for i in pausas_totais:
                    print(i.end_pause,i.start_pause)
                    somatorio += (i.end_pause.hour * 60 * 60 + i.end_pause.minute * 60 + i.end_pause.second) - (i.start_pause.hour * 60 * 60 + i.start_pause.minute * 60 + i.start_pause.second)
                    print(somatorio)
                seconds -= somatorio
            elif pause.start_pause and not pause.end_pause and Time_pause.objects.filter(match=match).count() > 1:
                seconds = (pause.start_pause.hour * 60 * 60 + pause.start_pause.minute * 60 + pause.start_pause.second) - (match.time_start.hour * 60 * 60 + match.time_start.minute * 60 + match.time_start.second)        
                print("Entrou no pausa iniciada não é a primeira")
                print("g:",seconds)
                status = 2
                for i in pausas_totais:
                    if i == pausas_totais.last():
                        break
                    somatorio += (i.end_pause.hour * 60 * 60 + i.end_pause.minute * 60 + i.end_pause.second) - (i.start_pause.hour * 60 * 60 + i.start_pause.minute * 60 + i.start_pause.second)
                seconds -= somatorio
            elif pause.start_pause and not pause.end_pause:
                print("Entrou no pausa iniciada, a primeira")
                status = 2
                seconds = (pause.start_pause.hour * 60 * 60 + pause.start_pause.minute * 60 + pause.start_pause.second) - (match.time_start.hour * 60 * 60 + match.time_start.minute * 60 + match.time_start.second)
        else:
            status = 1
            seconds = (rel.tm_hour * 60 * 60 + rel.tm_min * 60 + rel.tm_sec) - (match.time_start.hour * 60 * 60 + match.time_start.minute * 60 + match.time_start.second)
    else:
        seconds = 0
        status = 0
    print("Tempo: ",seconds, " status: ",status)
    return seconds, status