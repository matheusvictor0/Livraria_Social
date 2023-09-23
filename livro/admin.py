from django.contrib import admin
from .models import Livros

@admin.register(Livros)
class LivrosAdmin(admin.ModelAdmin):
    readonly_fields = ('isbn', 'nome', 'autor', 'capa_url', 'descricao', 'genero')
 