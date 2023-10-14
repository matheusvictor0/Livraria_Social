from django.db import models
from usuarios.models import Usuario

class Livros(models.Model):
    isbn = models.TextField(primary_key=True, unique=True)
    nome = models.CharField(max_length=100)
    autor = models.CharField(max_length=30)
    capa_url = models.URLField()
    descricao = models.TextField(max_length=100)
    genero = models.CharField(max_length=100, default="Outros") 
    avaliacao = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)

    class Meta:
        db_table = 'livro'

    def __str__(self) -> str:
            return self.nome
    
class Resenha(models.Model):
    usuario_id = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    livro = models.ForeignKey(Livros, on_delete=models.CASCADE)
    titulo = models.TextField()
    texto = models.TextField()
    avaliacao = models.IntegerField()
    
    def __str__(self):
        return f"Comentário sobre {self.livro.nome}"
 
class Lista_livros(models.Model):
    nome_lista = models.CharField(max_length=100)
    usuario_id = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    livros = models.ManyToManyField('Livros', related_name='livros_salvos')