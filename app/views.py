from django.shortcuts import render, redirect, get_object_or_404
from .models import Sexo, Player

# Create your views here.
def index(request):
    return render(request, 'index.html')

def player_manage(request):
    player = Player.objects.all()
    context = {
        'player': player,
    }
    return render(request, 'gerenciamento-jogadores.html', context)

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
        print(player)
        print("salvou?")
        return redirect('player_manage')

def player_edit(request, id):
    player = get_object_or_404(Player, id=id)
    context = {
        'player': player,
    }
    if request.method == 'GET':
        return render(request, 'editar-jogadores.html', context)
    elif 'excluir' in request.POST:
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
    return render(request, 'gerenciamento-times.html')

def team_register(request):
    return render(request, 'cadastro-times.html')

def team_edit(request):
    return render(request, 'editar-times.html')

def team_players_manage(request):
    return render(request, 'gerenciamento-jogadores-times.html')

def matches_manage(request):
    return render(request, 'gerenciamento-partidas.html')

def matches_edit(request):
    return render(request, 'editar-partidas.html')

def matches_register(request):
    return render(request, 'cadastro-partidas.html')

def add_player_team(request):
    return render(request, 'adicionar-jogadores-time.html')

def game(request):
    return render(request, 'jogo.html')

def sport(request):
    return render(request, 'esportes.html')
