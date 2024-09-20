from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index.html')

def cadastrojogadores(request):
    return render(request, 'cadastro-jogadores.html')