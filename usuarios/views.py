from django.shortcuts import render
from .models import Usuario
from django.shortcuts import redirect
from hashlib import sha256

def cadastro(request):
    status = request.GET.get('status')
    return render(request, 'cadastro.html', {'status': status})

def valida_cadastro(request):
    nome = request.POST.get('nome')
    email = request.POST.get('email')
    senha = request.POST.get('senha')
    senha_repeticao = request.POST.get('senha_repeticao')

    usuario = Usuario.objects.filter(email = email)

    if len(nome.strip()) == 0 or len(email.strip()) == 0:
        return redirect('/auth/cadastro/?status=1')

    if len(senha) < 8:
        return redirect('/auth/cadastro/?status=2')
    
    if senha != senha_repeticao:
        return redirect('/auth/cadastro/?status=5')
    
    if len(usuario) > 0:
        return redirect('/auth/cadastro/?status=3')
    try:
        senha = sha256(senha.encode()).hexdigest()
        usuario = Usuario(nome = nome, senha=senha, email=email)
        usuario.save()

        return redirect('/auth/cadastro/?status=0')
    except:
        return redirect('/auth/cadastro/?status=4')
