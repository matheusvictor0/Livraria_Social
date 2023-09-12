from django.shortcuts import render
from .models import Usuario
from django.http import HttpResponse
from django.shortcuts import redirect
from hashlib import sha256
from django.utils import timezone
from django.urls import reverse
from decouple import config
import secrets
from django.core.mail import send_mail

def login(request):
    status = request.GET.get('status') 
    return render(request, 'login.html', {'status': status,})

def cadastro(request):
    status = request.GET.get('status')
    return render(request, 'cadastro.html', {'status': status})

def valida_cadastro(request):
    nome = request.POST.get('nome')
    email = request.POST.get('email')
    senha = request.POST.get('senha')
    senha_repeticao = request.POST.get('senha_repeticao')

    # Verificar se o email já está em uso
    if Usuario.objects.filter(email=email).exists():
        return redirect('/auth/cadastro/?status=3')

    if len(nome.strip()) == 0 or len(email.strip()) == 0:
        return redirect('/auth/cadastro/?status=1')

    if len(senha) < 8:
        return redirect('/auth/cadastro/?status=2')

    if senha != senha_repeticao:
        return redirect('/auth/cadastro/?status=5')

    try:
        # Criar um novo usuário não confirmado
        senha = sha256(senha.encode()).hexdigest()
        usuario = Usuario(nome=nome, senha=senha, email=email, confirmado=False)

        # Gere um token de confirmação de email seguro
        token_confirmacao = secrets.token_urlsafe(32)
        usuario.token_confirmacao = token_confirmacao

        # Defina a data de expiração do token (opcional)
        usuario.data_expiracao_token = timezone.now() + timezone.timedelta(hours=24)

        usuario.save()

        # Envie um email de confirmação
        subject = 'Confirme seu email'
        message = f'Clique no link a seguir para confirmar seu email: {request.build_absolute_uri(reverse("confirmar_email", args=[usuario.id, token_confirmacao]))}'
        from_email = config('EMAIL_HOST_USER')
        recipient_list = [usuario.email]
        send_mail(subject, message, from_email, recipient_list)

        return redirect('/auth/cadastro/?status=0')
    except Exception as e:
        print(f"Erro em valida_cadastro: {str(e)}")
        return redirect('/auth/cadastro/?status=4')

def confirmar_email(request, user_id, token):
    try:
        # Procurar o usuário pelo ID
        usuario = Usuario.objects.get(id=user_id)

        # Verificar se o token de confirmação corresponde
        if token != usuario.token_confirmacao:
            return HttpResponse('Token de confirmação inválido.')

        # Marcar o usuário como confirmado
        usuario.confirmado = True
        usuario.save()

        return redirect('/auth/login/')  # Redirecionar para a página de login após a confirmação
    except Usuario.DoesNotExist:
        return HttpResponse('Usuário não encontrado.')
    