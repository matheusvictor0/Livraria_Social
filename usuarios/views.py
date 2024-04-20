from django.shortcuts import render
from .models import Usuario
from django.http import HttpResponse
from django.shortcuts import redirect
from hashlib import sha256
from django.utils import timezone
from django.urls import reverse
from django.utils.crypto import get_random_string
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

    # Verifica se o email já está em uso
    if Usuario.objects.filter(email=email).exists():
        return redirect('/auth/cadastro/?status=3')

    if len(nome.strip()) == 0 or len(email.strip()) == 0:
        return redirect('/auth/cadastro/?status=1')

    if len(senha) < 8:
        return redirect('/auth/cadastro/?status=2')

    if senha != senha_repeticao:
        return redirect('/auth/cadastro/?status=5')

    try:
        # Cria um novo usuário não confirmado
        senha = sha256(senha.encode()).hexdigest()
        usuario = Usuario(nome=nome, senha=senha, email=email, confirmado=False)

        token_confirmacao = secrets.token_urlsafe(32)
        usuario.token_confirmacao = token_confirmacao

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
        usuario = Usuario.objects.get(id=user_id)
        if token != usuario.token_confirmacao:
            return HttpResponse('Token de confirmação inválido.')
        usuario.confirmado = True
        usuario.save()

        return redirect('/auth/login/?status=0')
    except Usuario.DoesNotExist:
        return HttpResponse('Usuário não encontrado.')

def valida_login(request):
    email = request.POST.get('email')
    senha = request.POST.get('senha')
    senha = sha256(senha.encode()).hexdigest()

    usuario = Usuario.objects.filter(email=email).filter(senha=senha).first()

    if usuario is None:
        return redirect('/auth/login/?status=1')

    if not usuario.confirmado:
        return redirect('/auth/login/?status=2')

    request.session['usuario'] = usuario.id
    return redirect(f'/livro/home/')


def solicitar_redefinicao_senha(request):
    status = request.GET.get('status')
    usuario = None
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            usuario = Usuario.objects.get(email=email)
        except Usuario.DoesNotExist:
            status = '3'
        if usuario is not None:
            # Gerar um token de redefinição de senha
            token = get_random_string(length=32)
            usuario.token_confirmacao = token
            usuario.data_expiracao_token = timezone.now() + timezone.timedelta(hours=1)
            usuario.save()

            # Envie um email com o link de redefinição de senha
            subject = 'Redefinir Senha'
            message = f'Clique no link a seguir para redefinir sua senha: {request.build_absolute_uri(reverse("redefinir_senha", args=[token]))}'
            from_email = config('EMAIL_HOST_USER')
            recipient_list = [usuario.email]
            send_mail(subject, message, from_email, recipient_list)

            return redirect('/auth/solicitar_redefinicao_senha/?status=4')

    return render(request, 'solicitar_redefinicao_senha.html', {'status': status})

def redefinir_senha(request, token):
    status = request.GET.get('status')

    try:
        usuario = Usuario.objects.get(token_confirmacao=token)
    except Usuario.DoesNotExist:
        return HttpResponse('Token de redefinição de senha inválido ou expirado.')

    if request.method == 'POST':
        nova_senha = request.POST.get('nova_senha')
        senha_repeticao = request.POST.get('senha_repeticao')

        if nova_senha != senha_repeticao:
            return redirect(f'/auth/redefinir_senha/{token}/?status=1')

        if len(nova_senha) < 8:
            return redirect(f'/auth/redefinir_senha/{token}/?status=2')

        # Atualize a senha do usuário
        usuario.senha = sha256(nova_senha.encode()).hexdigest()
        usuario.token_confirmacao = None
        usuario.data_expiracao_token = None
        usuario.save()
        return redirect('/auth/login/?status=3')


    return render(request, 'redefinir_senha.html', {'token': token, 'status': status})

def sair(request):
    request.session.flush()
    return redirect('/auth/login/')

def perfil(request):
    status = request.GET.get('status')
    usuario_session = request.session.get('usuario')
    usuario = Usuario.objects.get(id=usuario_session)

    if request.method == "GET":
        return render(request, 'perfil.html', {'usuario': usuario, 'status': status})
    elif request.method == "POST":
        file = request.FILES.get("img_perfil")
        img = Usuario.objects.get(id=usuario, imagem_perfil=file)
        img.save()


def deletar_conta(request, id):
    if request.method == 'POST':  
        try:
            usuario = Usuario.objects.get(id=id)
            usuario.delete()
            return redirect('/auth/login/?status=5')
        except Usuario.DoesNotExist:
            return redirect('perfil')
