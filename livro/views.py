from django.shortcuts import redirect, render
from django.http import HttpResponse
from usuarios.models import Usuario
from .models import Livros, Resenha
from decouple import config
import requests

def buscar_dados_livro(query):
    api_key = config('API_KEY')
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

        # Tenta buscar o livro com base no ISBN
        livro, criado = Livros.objects.get_or_create(
            isbn=isbn,
            defaults={
                'nome': livro_detalhes.get('titulo', ''),
                'autor': livro_detalhes.get('autores', ''),
                'capa_url': livro_detalhes.get('capa_url', ''),
                'descricao': livro_detalhes.get('descricao', ''),
                'genero': livro_detalhes.get('genero', ''),
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
        categorias = categoria()

        return render(request, 'home.html', {'categoria_livro': categorias, 'usuario_logado': usuario})
    except Usuario.DoesNotExist:
        return redirect(f'/auth/login/?status=4')

def ver_livros(request, isbn):
    livro = Livros.objects.get(isbn = isbn)
    
    categorias = categoria()
    
    return render(request, 'ver_livros.html', {'livro': livro, 'categoria_livro': categorias,
                                               'usuario_logado': request.session.get('usuario')})

#Adicionar Resenha
def adicionar_resenha(request, isbn):
    livro = Livros.objects.get(isbn=isbn)
    if request.method == "POST":
        titulo_resenha = request.POST['titulo_resenha']
        texto_resenha = request.POST['texto_resenha']
        avaliacao_resenha = request.POST['avaliacao_resenha']

        usuario = Usuario.objects.get(id = request.session['usuario']) 

        # Cria a resenha associada ao livro
        resenha = Resenha(usuario_id=usuario, livro=livro, titulo=titulo_resenha, texto=texto_resenha, avaliacao=avaliacao_resenha)
        resenha.save()
        
        resenhas = Resenha.objects.filter(livro=livro)

        # Calcula a nova média das avaliações
        total_avaliacao = sum([r.avaliacao for r in resenhas])
        numero_resenhas = len(resenhas)
        nova_avaliacao_media = total_avaliacao / numero_resenhas
        media_avaliacao = round(nova_avaliacao_media, 1)

        # Atualiza a avaliação do livro com a nova média
        livro.avaliacao = media_avaliacao
        livro.save()
        
        categorias = categoria()

        return render(request, 'ver_livros.html', {'livro': livro, 'categoria_livro': categorias,
                                               'usuario_logado': usuario})
