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
]

