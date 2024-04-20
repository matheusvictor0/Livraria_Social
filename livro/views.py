from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Avg
from usuarios.models import Usuario
from datetime import date, timedelta, datetime
from .models import Livros, Resenha, Lista_livros, CurtidaResenha, Comentarios_Resenha
from django.shortcuts import get_object_or_404, redirect
from decouple import config
import requests

def buscar_dados_livro(query):
    api_key = config('API_KEY_LIVRO')
    url = f"https://www.googleapis.com/books/v1/volumes?q={query}&key={api_key}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        livros = []
        if "items" in data:
            for item in data["items"]:
                livro_data = item.get("volumeInfo", {})
                isbn_data = livro_data.get("industryIdentifiers", [])
                isbn = ""
                for identifier in isbn_data:
                    if identifier.get("type") == "ISBN_13":
                        isbn = identifier.get("identifier", "")
                        break
                                       
                livro_detalhes = {
                    'titulo': livro_data.get("title", "Título desconhecido"),
                    'autores': ", ".join(livro_data.get("authors", ["Autor desconhecido"])),
                    'capa_url': livro_data.get("imageLinks", {}).get("thumbnail", ""),
                    'descricao': livro_data.get("description", "Descrição indisponível"),
                    'genero': livro_data.get("categories", ["Outros"])[0] if livro_data.get("categories") else "Outros",
                    'isbn': isbn,
                }

                livros.append(livro_detalhes)
                if all(not livro['isbn'] for livro in livros):
                    return []

        return livros

    except requests.exceptions.RequestException as e:
        print(f"Erro na solicitação: {str(e)}")
    
def traduzir_texto(texto):
    api_key = config('API_KEY_TRADUTOR')
    url = f"https://translation.googleapis.com/language/translate/v2?key={api_key}"
    idioma_destino='pt'

    params = {
        'q': texto,
        'target': idioma_destino,
    }

    try:
        response = requests.post(url, params=params)
        response.raise_for_status()
        data = response.json()

        if 'data' in data and 'translations' in data['data']:
            primeira_traducao = data['data']['translations'][0]
            texto_traduzido = primeira_traducao['translatedText']
            return texto_traduzido

    except requests.exceptions.RequestException as e:
        print(f"Erro na solicitação: {str(e)}")

    return texto

# Função para buscar livros por título na API
def barra_buscar(request):
    livros = None

    if 'termo_pesquisa' in request.GET:
        termo_pesquisa = request.GET['termo_pesquisa']
        livros = buscar_dados_livro(termo_pesquisa)

    categorias = categoria()

    return render(request, "home.html", {'livros': livros, 'categoria_livro': categorias,
                                        'usuario_logado': request.session.get('usuario')})


# Função para adicionar um livro ao banco de dados por ISBN ou atualizá-lo
def adicionar_livro(request, isbn):
    livro_data = buscar_dados_livro(f"isbn:{isbn}")

    if livro_data:
        livro_detalhes = livro_data[0]
        descricao_traduzida = traduzir_texto(livro_detalhes.get('descricao', ''))
        genero_traduzido = traduzir_texto(livro_detalhes.get('genero', ''))
        
        livro, criado = Livros.objects.get_or_create(
            isbn=isbn,
            defaults={
                'nome': livro_detalhes.get('titulo', ''),
                'autor': livro_detalhes.get('autores', ''),
                'capa_url': livro_detalhes.get('capa_url', ''),
                'descricao': descricao_traduzida,
                'genero': genero_traduzido,
            }
        )
        return redirect('ver_livros', isbn=livro.isbn)
    
#função de buscar todas a categorias
def categoria():
    livros = Livros.objects.all()
    if livros:
        categorias = set()
        for livro in livros:
            genero = livro.genero
            categorias.add(genero)
        
        return categorias
    return None

def home(request):
    if 'usuario' not in request.session:
        return redirect(f'/auth/login/?status=4')

    usuario_id = request.session['usuario']

    try:
        usuario = Usuario.objects.get(id=usuario_id)
        livros = Livros.objects.all()
        categorias = categoria()

        # Calcule a média das avaliações para cada livro
        livros = Livros.objects.annotate(avaliacao_media=Avg('resenha__avaliacao'))
        livros = livros.order_by('avaliacao_media')
        
        # Obtem os 10 melhores
        melhores_livros = livros[:10]

        #Obtem as resenhas mais curtidas
        resenhas_mais_curtidas = Resenha.objects.all().order_by('-curtidas')[:10]

        return render(request, 'home.html', {'categoria_livro': categorias, 'livros': livros, 'usuario_logado': usuario, 
                                             'melhores_livros': melhores_livros, 'resenhas_mais_curtidas': resenhas_mais_curtidas})
    except Usuario.DoesNotExist:
        return redirect(f'/auth/login/?status=4')


def favoritar_livro(request,isbn):
    if request.method == 'POST':
        usuario = Usuario.objects.get(id = request.session['usuario']) 
        nome = "Favoritos"
        livro = Livros.objects.get(isbn=isbn)
        lista = Lista_livros.objects.get(nome_lista=nome, usuario_id=usuario)
        if lista.livros.filter(pk=livro.pk).exists():
            lista.livros.remove(livro)
        else:
            lista.livros.add(livro)

    return redirect('ver_livros', isbn=isbn)

def filtrar_livros_por_categoria(request):
    categorias = categoria()
    
    livros_filtrados = []
    if request.method == 'GET':
        categoria_pesquisar = request.GET.get('categoria')  
        if categoria_pesquisar and categoria_pesquisar != 'Categorias':
            livros_banco = list(Livros.objects.filter(genero=categoria_pesquisar))  
        else:
            livros_banco = list(Livros.objects.all())

        livros_api = buscar_dados_livro(f"categories:{categoria_pesquisar}")
        livros_filtrados = livros_api + livros_banco

        return render(request, 'home.html', {'livros': livros_filtrados, 'categoria_livro': categorias})
    else:
        return render(request, 'home.html', {'categoria_livro': categorias})

def ver_livros(request, isbn):
    status = request.GET.get('status')

    usuario = Usuario.objects.get(id = request.session['usuario']) 
    livro = Livros.objects.get(isbn = isbn)
    resenhas = Resenha.objects.filter(livro=livro)

    curtidas = []
    for resenha in resenhas:
        if resenha.user_has_liked(usuario):
            curtidas.append(True)
        else:
            curtidas.append(False)
        
    resenhas_combinada = zip(resenhas, curtidas)

    nome_lista = "Favoritos"
    listas_banco = Lista_livros.objects.filter(nome_lista=nome_lista, usuario_id=usuario)

    if listas_banco:
        lista = Lista_livros.objects.get(nome_lista=nome_lista, usuario_id=usuario)
        if lista.livros.filter(pk=livro.pk).exists():
            favoritado = 1
        else:
            favoritado = 0
    else:
        lista = Lista_livros(nome_lista=nome_lista, usuario_id=usuario)
        lista.save()
        favoritado = 0

    # Calcule a nova média das avaliações
    total_avaliacao = sum([r.avaliacao for r in resenhas])
    numero_resenhas = len(resenhas)

    if numero_resenhas > 0:
        nova_avaliacao_media = total_avaliacao / numero_resenhas
        media_avaliacao = round(nova_avaliacao_media, 1)
    else:
        media_avaliacao = 0
        
    # Atualize a avaliação do livro com a nova média
    livro.avaliacao = media_avaliacao
    livro.save()

    listas = Lista_livros.objects.filter(usuario_id = usuario)
    categorias = categoria()
    
    return render(request, 'ver_livros.html', {'livro': livro, 'categoria_livro': categorias,
    'usuario_logado': usuario, 'listas': listas, 'favoritado': favoritado, 'resenhas_combinada': resenhas_combinada, 'status': status})

#função de adicionar Resenha
def adicionar_resenha(request, isbn):
    
    livro = Livros.objects.get(isbn=isbn)
    if request.method == "POST":
        titulo_resenha = request.POST['titulo_resenha']
        texto_resenha = request.POST['texto_resenha']
        avaliacao_resenha = request.POST['avaliacao_resenha']
        data = date.today()
        
        usuario = Usuario.objects.get(id = request.session['usuario']) 

        resenha = Resenha(usuario_id=usuario, livro=livro, titulo=titulo_resenha, texto=texto_resenha, avaliacao=avaliacao_resenha, data=data)
        resenha.save()
        
        return redirect('ver_livros', isbn=isbn)

def curtir_resenha(request, resenha_id, isbn):

    if request.method == "POST":
        resenha = Resenha.objects.get(pk=resenha_id)
        usuario = Usuario.objects.get(id=request.session['usuario'])
    
        try:
            curtida = CurtidaResenha.objects.get(usuario=usuario, resenha=resenha)
            if curtida.curtida:
                resenha.descurtir(usuario)
                curtida.delete()
            else:
                resenha.curtir()
                curtida.curtida = True
                curtida.save()
        except CurtidaResenha.DoesNotExist:
            resenha.curtir()
            CurtidaResenha.objects.create(usuario=usuario, resenha=resenha, curtida=True)
    
        url = reverse('ver_livros', args=[isbn])
        return HttpResponseRedirect(f'{url}?like={resenha.id}')
    
    return redirect('ver_livros', isbn=isbn)

def editar_resenha(request, resenha_id):
    if request.method == 'POST':
        resenha = Resenha.objects.get(id=resenha_id)
        resenha.titulo = request.POST['titulo_resenha']
        resenha.texto = request.POST['texto_resenha']
        resenha.avaliacao = request.POST['avaliacao_resenha']
        resenha.save()

        return redirect('ver_livros', isbn=resenha.livro.isbn)

def excluir_resenha(request, resenha_id):
    if request.method == 'POST':  
        try:
            resenha = Resenha.objects.get(id=resenha_id)
            isbn = resenha.livro.isbn
            resenha.delete()
            return redirect('ver_livros', isbn=isbn)
        except Lista_livros.DoesNotExist:
            return redirect('ver_livros', isbn=isbn)
        

def comentar_resenha(request, resenha_id):
    if request.method == "POST":
        texto = request.POST['texto_comentario']
        usuario = Usuario.objects.get(id = request.session['usuario']) 
        resenha = Resenha.objects.get(pk=resenha_id)
        data = date.today()
        comentario = Comentarios_Resenha(usuario=usuario, resenha_id=resenha, texto=texto, data=data)
        comentario.save()

        resenha = Resenha.objects.get(id=resenha_id)
        resenha.comentarios.add(comentario)
        isbn = resenha.livro.isbn
        
        url = reverse('ver_livros', args=[isbn])
        return HttpResponseRedirect(f'{url}?resenha={resenha_id}&comment={comentario.id}')


    return redirect('ver_livros', isbn=isbn)

def excluir_comentario(request, comentario_id):
    if request.method == 'POST':  
        comentario = get_object_or_404(Comentarios_Resenha, id=comentario_id)
        isbn = comentario.resenha_id.livro.isbn
        comentario.delete()

    return redirect('ver_livros', isbn=isbn)
    

def editar_comentario(request, comentario_id):
    if request.method == 'POST':
        comentario = Comentarios_Resenha.objects.get(id=comentario_id)
        comentario.texto = request.POST['texto_edit_comentario']
        comentario.save()
        isbn = comentario.resenha_id.livro.isbn

        return redirect('ver_livros', isbn=isbn)
  
def salvar_livro(request, isbn):
    status = request.GET.get('status')
    url = reverse('ver_livros', kwargs={'isbn': isbn})
    
    if request.method == 'POST':
        usuario = Usuario.objects.get(id=request.session['usuario'])
        listas = Lista_livros.objects.filter(usuario_id=usuario)
        nome_listas = request.POST.getlist('listas_selecionadas')
        livro = Livros.objects.get(isbn=isbn)
        if nome_listas:
            for lista_id in nome_listas:
                lista = Lista_livros.objects.get(id=lista_id)
                lista.livros.add(livro)
            return redirect(f'{url}?status=0')
        else:
            return redirect(f'{url}?status=1')
           
    return render(request, 'ver_livros.html', {'livro': livro, 'listas': listas, 'status': status})

def criar_lista(request, isbn):
    status = request.GET.get('status')
    url = reverse('ver_livros', kwargs={'isbn': isbn})
    if request.method == 'POST':
        nome_da_lista = request.POST.get('nova_lista')
        usuario = Usuario.objects.get(id=request.session['usuario'])
        listas = Lista_livros.objects.filter(usuario_id=usuario)
        livro = Livros.objects.get(isbn=isbn)

        if nome_da_lista:
            listas_banco = Lista_livros.objects.filter(nome_lista=nome_da_lista, usuario_id=usuario)
            if listas_banco:
                return redirect(f'{url}?status=2')
            else:
                nova_lista = Lista_livros.objects.create(nome_lista=nome_da_lista, usuario_id=usuario)
                nova_lista.save()
                
                return HttpResponseRedirect(f'{url}?dropdown=open')

    return render(request, 'ver_livros.html', {'livro': livro, 'listas': listas, 'usuario_logado': usuario, 'status': status})

def minhas_listas(request):
    status = request.GET.get('status')
    usuario = request.session.get('usuario')
    listas = Lista_livros.objects.filter(usuario_id = usuario)
    
    return render(request, 'minhas_listas.html', {'usuario_logado': usuario, 'listas': listas, 'status': status})

def editar_lista(request, id):
    url = reverse('minhas_listas')
    status = request.GET.get('status')
    if request.method == 'POST':
        nome_novo = request.POST['nome_lista']
        listas_banco = Lista_livros.objects.filter(nome_lista=nome_novo)
        if listas_banco:
            return redirect(f'{url}?status=0')
        else:
            lista = Lista_livros.objects.get(id=id)
            lista.nome_lista = nome_novo
            lista.save()
            return redirect('minhas_listas')
    
    return redirect('minhas_listas', status=status)

def excluir_lista(request, id):
    if request.method == 'POST':  
        try:
            lista = get_object_or_404(Lista_livros, id=id)
            lista.delete()
            return redirect('minhas_listas')
        except Lista_livros.DoesNotExist:
            return redirect('minhas_listas')

def excluir_livro_lista(request, isbn, id):
    if request.method == 'POST':  
        lista = get_object_or_404(Lista_livros, id=id)
        livro = get_object_or_404(Livros, isbn=isbn)

        # Verifica se o livro está na lista
        if livro in lista.livros.all():
            lista.livros.remove(livro)
            return redirect('minhas_listas')

def atualizar_melhores_resenhas():
    resenhas_mais_curtidas = Resenha.objects.all().order_by('-curtidas')[:6]
    data_atual = datetime.now().date()

    for resenha in resenhas_mais_curtidas:
        if (resenha.data_final is None) or (resenha.data_final <= data_atual):
            resenha.melhor_resenha += 1
            resenha.data_atual = data_atual
            resenha.data_final = data_atual + timedelta(days=7)
            resenha.save()

def minhas_resenhas(request):
    status = request.GET.get('status')
    usuario = request.session.get('usuario')

    atualizar_melhores_resenhas()

    resenhas = Resenha.objects.filter(usuario_id = usuario)
    
    total_resenhas = resenhas.count()

    total_curtidas = 0
    total_melhor_resenha = 0
    for resenha in resenhas:
        total_curtidas += resenha.curtidas 
        total_melhor_resenha += resenha.melhor_resenha
    
    return render(request, 'minhas_resenhas.html', {'usuario_logado': usuario, 'resenhas': resenhas, 'total_resenhas': total_resenhas, 'total_curtidas': total_curtidas, 'total_melhor_resenha': total_melhor_resenha, 'status': status})
