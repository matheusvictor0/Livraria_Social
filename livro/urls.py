from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    #path('ver_livro/<str:isbn>', views.ver_livros, name='ver_livros'),
    path('', views.barra_buscar, name='buscar'),
    path('adicionar_livro/<str:isbn>/', views.adicionar_livro, name='adicionar_livro'),

]

