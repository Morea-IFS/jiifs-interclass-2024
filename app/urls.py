from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name = "Home"),
    path('cadastrojogadores/', views.cadastrojogadores, name = "CadastroJogadores"),
]