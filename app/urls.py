from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name = "Home"),
    path('gerenciamento-jogadores/', views.gerenciamento, name = "Gerenciamento"),
    path('gerenciamento-times/', views.gerenciamentotimes, name = "Gerenciamento-Times"),
    path('cadastro-jogadores/', views.cadastrojogadores, name = "Cadastro-Jogadores"),
    path('cadastro-times/', views.cadastrotimes, name = "Cadastro-Times"),
    path('editar-jogadores/', views.editarjogadores, name = "Editar-Jogadores"),
    path('editar-times/', views.editartimes, name = "Editar-Times"),
    path('jogo/', views.jogo, name = "Jogo"),
    path('esportes/', views.esportes, name = "Esportes"),
]