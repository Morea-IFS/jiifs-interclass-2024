from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index.html')

def player_manage(request):
    return render(request, 'gerenciamento-jogadores.html')

def team_manage(request):
    return render(request, 'gerenciamento-times.html')

def player_register(request):
    return render(request, 'cadastro-jogadores.html')

def team_register(request):
    return render(request, 'cadastro-times.html')

def player_edit(request):
    return render(request, 'editar-jogadores.html')

def team_edit(request):
    return render(request, 'editar-times.html')

def game(request):
    return render(request, 'jogo.html')

def sport(request):
    return render(request, 'esportes.html')
