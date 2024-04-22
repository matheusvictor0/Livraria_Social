from .models import Lista_livros, Resenha, Livros
from collections import Counter

def recomendar_por_favoritos(usuario):
    livros_favoritos = Lista_livros.objects.get(nome_lista="Favoritos", usuario_id=usuario).livros.all()
    
    generos = []
    autores = []
    for livro in livros_favoritos:
        resenha_usuario = Resenha.objects.filter(usuario_id=usuario, livro=livro).first()
        if not resenha_usuario or resenha_usuario.avaliacao >= 4:
            generos.append(livro.genero)
            autores.append(livro.autor)
    
    return generos, autores
        
def recomendar_por_livros_salvos(usuario):
    listas_livros_salvos = Lista_livros.objects.filter(usuario_id=usuario).exclude(nome_lista="Favoritos")

    generos = []
    autores = []
    for lista in listas_livros_salvos:
        for livro in lista.livros.all():

            resenha_usuario = Resenha.objects.filter(usuario_id=usuario, livro=livro).first()

            # Verifica se não há uma resenha/avaliação para o livro
            if not resenha_usuario or resenha_usuario.avaliacao >= 4:
                generos.append(livro.genero)
                autores.append(livro.autor)
        
    return generos, autores

def filtrar_livros(lista, campo, usuario):
    cont_itens = Counter(lista)
    top_itens = [item for item, _ in cont_itens.most_common(3)]

    livros_recomendados = []

    for item in top_itens:
        # Obter livros com base no tipo (autor ou gênero), ordenados por avaliação decrescente
        if campo == "autor":
            livros = Livros.objects.filter(autor=item).order_by('-avaliacao')
        elif campo == "genero":
            livros = Livros.objects.filter(genero=item).order_by('-avaliacao')
        
        livros_validos = []

        for livro in livros:
            # Filtrar para excluir livros salvos em listas do usuário
            livro_em_lista = Lista_livros.objects.filter(usuario_id=usuario, livros=livro).exists()
            # Verificar se o livro já foi resenhado/avaliado pelo usuário
            livro_com_resenha = Resenha.objects.filter(usuario_id=usuario, livro=livro).exists()

            if not livro_em_lista and not livro_com_resenha:
                livros_validos.append(livro)

        # Adicionar os dois melhores após aplicar a filtragem
        if len(livros_validos) > 2 and len(top_itens) == 3:
            livros_recomendados.extend(livros_validos[:2])
        else:
            livros_recomendados.extend(livros_validos[:5])
    return livros_recomendados

def recomendar_livros(usuario):
    generos = [] 
    autores = []
    generos_favoritos, autores_favoritos = recomendar_por_favoritos(usuario)
    generos_salvos, autores_salvos = recomendar_por_livros_salvos(usuario)

    # Combinar todos os gêneros e autores
    generos = generos_favoritos + generos_salvos
    autores = autores_favoritos + autores_salvos

    livros_recomendados_genero = filtrar_livros(generos, "genero", usuario)
    livros_recomendados_autor = filtrar_livros(autores, "autor", usuario)

    livros_recomendados = list(set(livros_recomendados_genero + livros_recomendados_autor))

    return livros_recomendados

def usuarioInteragiu(usuario):
    livro_em_lista = Lista_livros.objects.filter(usuario_id=usuario).exists()
    livro_com_resenha = Resenha.objects.filter(usuario_id=usuario).exists()

    if livro_em_lista or livro_com_resenha:
        return True
    
    
