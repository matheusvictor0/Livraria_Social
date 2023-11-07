from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('ver_livro/<str:isbn>', views.ver_livros, name='ver_livros'),
    path('criar_lista/<str:isbn>', views.criar_lista, name='criar_lista'),
    path('salvar_livro/<str:isbn>', views.salvar_livro, name='salvar_livro'),
    path('', views.barra_buscar, name='buscar'),
    path('adicionar_livro/<str:isbn>/', views.adicionar_livro, name='adicionar_livro'),
    path('adicionar_resenha/<str:isbn>/', views.adicionar_resenha, name='adicionar_resenha'),
    path('favoritar_livro/<str:isbn>/', views.favoritar_livro, name='favoritar_livro'),
    
    path('minhas_listas/', views.minhas_listas, name='minhas_listas'),
    path('editar_lista/<str:id>/', views.editar_lista, name='editar_lista'),
    path('excluir_lista/<str:id>/', views.excluir_lista, name='excluir_lista'),
    path('excluir_livro_lista/<str:isbn>/<int:id>', views.excluir_livro_lista, name='excluir_livro_lista'),

    path('curtir_resenha/<int:resenha_id>/<str:isbn>', views.curtir_resenha, name='curtir_resenha'),
    path('editar_resenha/<int:resenha_id>/', views.editar_resenha, name='editar_resenha'),
    path('excluir_resenha/<int:resenha_id>/', views.excluir_resenha, name='excluir_resenha'),

    path('comentar_resenha/<int:resenha_id>/', views.comentar_resenha, name='comentar_resenha'),
    path('editar_comentario/<int:comentario_id>/', views.editar_comentario, name='editar_comentario'),
    path('excluir_comentario/<int:comentario_id>/', views.excluir_comentario, name='excluir_comentario'),

]

