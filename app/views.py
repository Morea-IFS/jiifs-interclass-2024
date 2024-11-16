from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from .models import Volley_match, Player, Penalties, Time_pause, Team, Sport, Point, Team_sport, Player_team_sport, Match, Team_match, Player_match, Assistance
from django.db.models import Count
from django.contrib import messages
from django.db import IntegrityError
from django.conf import settings
import time
# Create your views here.
def index(request):
    return render(request, 'index.html')

def player_manage(request):
    player = Player.objects.all()
    if not player:
        print("Não há nenhum jogador cadastrado!")
    return render(request, 'player_manage.html', {'player': player})

def team_manage(request):
    teste = Team.objects.all()
    team_sports = Team_sport.objects.select_related('team', 'sport').all()
    return render(request, 'team_manage.html', {'team_sports': team_sports, 'teste': teste,})

def team_players_manage(request, id):
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
        return redirect('team_players_manage', id=team.id)

def matches_manage(request):
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
    if not context:
        print("Não há nenhuma partida cadastrada!")
    return render(request, 'matches_manage.html',{'context': context,})

def matches_edit(request, id):
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
        else:
            try:
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
    if request.method == 'GET':
        return render(request, 'player_register.html')
    else:
        try:
            name = request.POST.get('name')
            instagram = request.POST.get('instagram')
            sexo = request.POST.get('sexo')
            photo = request.FILES.get('photo')
            player = Player.objects.create(name=name, instagram=instagram, sexo=sexo, photo=photo)
            player.save()
        except (TypeError, ValueError):
            messages.error(request, 'Um valor foi informado incorretamente!')
        except IntegrityError as e:
            messages.error(request, 'Algumas informações não foram preenchidas :(')
        except Exception as e:
            messages.error(request, f'Um erro inesperado aconteceu: {str(e)}')
        return redirect('player_register')

def team_register(request):
    sport = Sport.objects.all()
    if request.method == 'GET':
        return render(request, 'team_register.html', {'sport': sport,})
    else:
        try:
            name = request.POST.get('name')
            hexcolor = request.POST.get('hexcolor')
            # sexo = request.POST.get('sexo')
            photo = request.FILES.get('photo')
            list_sport = request.POST.getlist('input-checkbox')
            team = Team.objects.create(name=name, hexcolor=hexcolor, photo=photo)
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
        except (TypeError, ValueError):
            messages.error(request, 'Um valor foi informado incorretamente!')
        except IntegrityError as e:
            messages.error(request, 'Algumas informações não foram preenchidas :(')
        except Exception as e:
            messages.error(request, f'Um erro inesperado aconteceu: {str(e)}')
    return redirect('team_manage') 

def games(request):
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
    sport = Sport.objects.all()
    if not sport:
        print("Não há nenhum time cadastrado!")
    return render(request, 'sport_manage.html',{'sport': sport,})

def sport_edit(request, id):
    sport = get_object_or_404(Sport, id=id)
    if request.method == "GET":
        return render(request, 'sport_edit.html', {'sport': sport,})
    elif 'excluir' in request.POST:
        sport.delete()
        return redirect('sport_manage')
    else:
        try:
            sport.name = request.POST.get('name')
            sport.max_titulares = request.POST.get('max_titulares')
            sport.sets = request.POST.get('sets')
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
    if request.method =="GET":
        return render(request, 'sport_register.html')
    else:
        try:
            name = request.POST.get('name')
            max_titulares = request.POST.get('max_titulares')
            sets = request.POST.get('sets')
            Sport.objects.create(name=name, max_titulares=max_titulares, sets=sets)
            print(request.POST)
        except (TypeError, ValueError):
            messages.error(request, 'Um valor foi informado incorretamente!')
        except IntegrityError as e:
            messages.error(request, 'Algumas informações não foram preenchidas :(')
        except Exception as e:
            messages.error(request, f'Um erro inesperado aconteceu: {str(e)}')
        return redirect('sport_register')
    
def general_data(request, id):
    match = get_object_or_404(Match, id=id)
    team_matchs = Team_match.objects.filter(match=match)
    team_match_a = team_matchs[0]
    team_match_b = team_matchs[1]
    point_a = Point.objects.filter(team_match=team_match_a).count()
    point_b = Point.objects.filter(team_match=team_match_b).count()
    if request.method =="GET":
        context = {
            'match': match,
        }
        return render(request, 'general_data.html', context)
    else:
        if Match.objects.filter(status=1) and match.status != 1:
            context = {
                'match': match,
                'error_mensage':'Essa ação não pode ser realizada, já existe uma partida acontecendo!',
            }
            print("Essa ação não pode ser realizada.")
            return render(request,'general_data.html', context)
            
        else:
            match.status = request.POST.get('status')
            if match.status == '2':
                if point_a > point_b:
                    match.Winner_team = team_match_a.team
                elif point_b > point_a:
                    match.Winner_team = team_match_b.team
            match.save()
            return redirect('games')

def scoreboard(request):
    match = Match.objects.get(status=1)
    team_matchs = Team_match.objects.filter(match=match)
    players_match = Player_match.objects.filter(match=match)
    team_match_a = team_matchs[0]
    team_match_b = team_matchs[1]
    players_match_a = players_match.filter(team_match=team_match_a)
    players_match_b = players_match.filter(team_match=team_match_b)
    points = Point.objects.filter(team_match=team_match_a).union(
        Point.objects.filter(team_match=team_match_b)
    ).order_by('time')
    point_a = Point.objects.filter(team_match=team_match_a).count()
    point_b = Point.objects.filter(team_match=team_match_b).count()
    context = {
        'match': match,
        'team_match_a':team_match_a,
        'team_match_b':team_match_b,
        'players_match_a':players_match_a,
        'players_match_b':players_match_b,
        'team_matchs':team_matchs,
        'points':points,
        'point_a':point_a,
        'point_b':point_b,
    }
    if request.method == "GET":
        if match.status == 1:
            return render(request, 'scoreboard.html', context)
    elif request.method == "POST":
        try:
            if 'team_a_add' in request.POST:
                player_select = request.POST.get('player_point')
                if player_select == "0" :
                    Point.objects.create(team_match=team_match_a, point_types=1)
                else:
                    player = Player.objects.get(id=player_select)
                    Point.objects.create(team_match=team_match_a, point_types=1, player=player)              
                return redirect('scoreboard')
                
            elif 'team_b_add' in request.POST:
                player_select = request.POST.get('player_point')
                if player_select == "0" :
                    Point.objects.create(team_match=team_match_b, point_types=1)
                else:
                    player = Player.objects.get(id=player_select)
                    Point.objects.create(team_match=team_match_b, point_types=1, player=player)              
                return redirect('scoreboard')
            
            elif 'team_a_remove' in request.POST:
                if Point.objects.filter(team_match=team_match_a):
                    point_a_remove = Point.objects.filter(team_match=team_match_a)
                    point_a_remove_last = point_a_remove.last()
                    point_a_remove_last.delete()
                return redirect('scoreboard')
            elif 'team_b_remove' in request.POST:
                if Point.objects.filter(team_match=team_match_b):
                    point_b_remove = Point.objects.filter(team_match=team_match_b)
                    point_b_remove_last = point_b_remove.last()
                    point_b_remove_last.delete()
                return redirect('scoreboard')
            elif 'type_penalties' in request.POST:
                type_penalties = request.POST.get('type_penalties')
                player = get_object_or_404(Player, id=request.POST.get('player_penalties'))
                print("player: ",player)
                player_penalties = Player_match.objects.get(player=player, match=match)
                print("player penalties: ",player_penalties)
                Penalties.objects.create(type_penalties=type_penalties, player=player_penalties.player, team_match=player_penalties.team_match)
                return redirect('scoreboard')
            elif 'point_assistance' in request.POST:
                point = get_object_or_404(Point, id=request.POST.get('point_assistance'))
                player = get_object_or_404(Player, id=request.POST.get('player_assistance'))
                Assistance.objects.create(assis_to=point,player=player, match=match)
                return redirect('scoreboard')
            elif 'status' in request.POST:
                print("status")
                match.status = request.POST.get('status')
                match.save()
                if match.status == 1:
                    return redirect('scoreboard')
                else:
                    return redirect('games')
            elif 'add_time' in request.POST:
                match.add = request.POST.get('add_time')
                match.save()
                print(match.add)
                print(match.status)
                return redirect('scoreboard')
            elif 'time_init' in request.POST:
                time_ai = time.localtime()
                match.time_start = time.strftime("%H:%M:%S", time_ai)
                match.save()
                return redirect('scoreboard')
            elif 'time_stop' in request.POST:
                time_as = time.localtime()
                match.time_end = time.strftime("%H:%M:%S", time_as)
                match.save()
                return redirect('scoreboard')
            elif 'time_pause' in request.POST:
                if match.time_start and match.time_end:
                    print("Tempo já foi finalizado!")
                    messages.warning(request, "O cronometro já foi finalizado.")
                    return redirect('scoreboard')
                elif match.time_start:
                    print("Tempo já foi iniciado")
                    time_pause = time.localtime()
                    if Time_pause.objects.filter(match=match):                
                        ultimo = Time_pause.objects.filter(match=match).last()
                        if ultimo.start_pause and ultimo.end_pause:
                            create_pause = Time_pause.objects.create(start_pause=time.strftime("%H:%M:%S", time_pause), match=match)
                            create_pause.save()
                            print("somenteterminou", ultimo.id," o novo: ", create_pause.id)
                            return redirect('scoreboard')
                        else:
                            ultimo.end_pause = time.strftime("%H:%M:%S", time_pause)
                            ultimo.save()
                            print("somente comecou", ultimo.id)
                            return redirect('scoreboard')
                    else:
                        created_pause = Time_pause.objects.create(start_pause=time.strftime("%H:%M:%S", time_pause), match=match)
                        created_pause.save()
                        return redirect('scoreboard')
                else:
                    print("Tempo não foi iniciado para ser pausado!")
                    messages.error(request, "Você precisa iniciar o tempo!")
                    return redirect('scoreboard')
        except (TypeError, ValueError):
            messages.error(request, 'Um valor foi informado incorretamente!')
        except IntegrityError as e:
            messages.error(request, 'Algumas informações não foram preenchidas :(')
        except Exception as e:
            messages.error(request, f'Um erro inesperado aconteceu: {str(e)}')
        return redirect('scoreboard')
        



def players_in_teams(request, id):
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
                if int(number) < 1:
                    messages.error(request, "Os números precisam ser maior que 1!")
                    return redirect('add_players_match', id)
                else:
                    print(request.POST.get(f'number_{i}'))
                    number = request.POST.get(f'number_{i}')               
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
    



def timer(request):
    return render(request, 'timer.html')

def scoreboard_public(request):
    if Match.objects.filter(status=1):
        match = Match.objects.get(status=1)
        team_matchs = Team_match.objects.filter(match=match)
        team_match_a = team_matchs[0]
        team_match_b = team_matchs[1]
        players_match_a = Player_match.objects.filter(team_match=team_match_a)
        players_match_b = Player_match.objects.filter(team_match=team_match_b)
        point_a = Point.objects.filter(team_match=team_match_a).count()
        point_b = Point.objects.filter(team_match=team_match_b).count()
        context = {
            'match': match,
            'team_match_a':team_match_a,
            'team_match_b':team_match_b,
            'players_match_a':players_match_a,
            'players_match_b':players_match_b,
            'point_a':point_a,
            'point_b':point_b,
        }
        return render(request, 'scoreboard_public.html', context)
    else:
        return render(request, 'scoreboard_public.html')