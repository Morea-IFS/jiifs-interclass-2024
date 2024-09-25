from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index.html')

def gerenciamento(request):
    return render(request, 'gerenciamento-jogadores.html')

def gerenciamentotimes(request):
    return render(request, 'gerenciamento-times.html')

def cadastrojogadores(request):
    return render(request, 'cadastro-jogadores.html')

def cadastrotimes(request):
    return render(request, 'cadastro-times.html')

def editarjogadores(request):
    return render(request, 'editar-jogadores.html')

def editartimes(request):
    return render(request, 'editar-times.html')

def jogo(request):
    return render(request, 'jogo.html')

def esportes(request):
    return render(request, 'esportes.html')
