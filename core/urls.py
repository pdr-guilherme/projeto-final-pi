from django.urls import path
from . import views

urlpatterns = [
    # Rota principal (Home)
    path('', views.home, name='home'),
    
    # Rotas de cadastro
    path('cadastro/lancamento/', views.cadastro_lancamento, name='cadastro_lancamento'),
    path('cadastro/auxiliar/', views.cadastro_auxiliar, name='cadastro_auxiliar'),
    
    # Rotas de detalhes
    path('disco/detalhes/', views.detalhe_lancamento, name='detalhe_lancamento'),
    path('artista/detalhes/', views.detalhe_artista, name='detalhe_artista'),
    
    # Rotas de usuário
    path('perfil/', views.perfil, name='perfil'),
    path('login/', views.login_view, name='login'),
]