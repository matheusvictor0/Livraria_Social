from django.db import models

class Livros(models.Model):
    isbn = models.TextField(primary_key=True, unique=True)
    nome = models.CharField(max_length=100)
    autor = models.CharField(max_length=30)
    capa_url = models.URLField()
    descricao = models.TextField(max_length=100)
    genero = models.CharField(max_length=100, default="Outros") 

    class Meta:
        db_table = 'livro'  # Especifica o nome da tabela como 'livro'

    def __str__(self) -> str:
            return self.nome