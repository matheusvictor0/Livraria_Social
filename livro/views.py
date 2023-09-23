from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.http import HttpResponse
from usuarios.models import Usuario
from .models import Livros
from decouple import config
import requests


#função de buscar livro na api
def buscar_livro(titulo):
    livro = None
    api_key = config('API_KEY')
    url = f"https://www.googleapis.com/books/v1/volumes?q={titulo}&key={api_key}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if "items" in data:
            livro_data = data["items"][0].get("volumeInfo", {})
            titulo = livro_data.get("title", "Título desconhecido")
            autores = ", ".join(livro_data.get("authors", ["Autor desconhecido"]))
            capa_url = livro_data.get("imageLinks", {}).get("thumbnail", "")
            descricao = livro_data.get("description", "Descrição indisponível")
            categorias = livro_data.get("categories", ["Outros"])  

            # Pega o primeiro gênero da lista de categorias (se houver)
            genero = categorias[0] if categorias else "Outros"

            # Obtém os dados de ISBN
            isbn_data = livro_data.get("industryIdentifiers", [])
            isbn = ""
            for identifier in isbn_data:
                if identifier.get("type") == "ISBN_13":
                    isbn = identifier.get("identifier", "")
                    break  

            livro = {
                'titulo': titulo,
                'autores': autores,
                'capa_url': capa_url,
                'descricao': descricao,
                'genero': genero,
                'isbn': isbn,  
            }

            return livro


    except requests.exceptions.RequestException as e:
        print(f"Erro na solicitação: {str(e)}")
        return None

#função de buscar livro
def barra_buscar(request):
    livro = None
    livro_data = None

    if 'termo_pesquisa' in request.GET:
        termo_pesquisa = request.GET['termo_pesquisa']
        livro_data = buscar_livro(termo_pesquisa)

    if livro_data:
        livro_obj, created = Livros.objects.get_or_create(isbn=livro_data['isbn'], defaults={
            'nome': livro_data['titulo'],
            'autor': livro_data['autores'],
            'capa_url': livro_data['capa_url'],
            'descricao': livro_data['descricao'],
            'genero': livro_data['genero'],
        })


        livro = livro_obj
    
    categorias = categoria()

    #Mudar rederecionamento para ver_livro
    return render(request, "home.html", {'livro': livro, 'categoria_livro': categorias,
                                               'usuario_logado': request.session.get('usuario')})


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





