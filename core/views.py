from django.shortcuts import render

def home(request):
    return render(request, 'core/home.html')

def cadastro_lancamento(request):
    return render(request, 'core/cadastro_lancamento.html')

def detalhe_lancamento(request):
    return render(request, 'core/detalhe_lancamento.html')

def detalhe_artista(request):
    return render(request, 'core/detalhe_artista.html')

def perfil(request):
    return render(request, 'core/perfil.html')

def cadastro_auxiliar(request):
    return render(request, 'core/cadastro_auxiliar.html')

def login_view(request):
    return render(request, 'core/login.html')