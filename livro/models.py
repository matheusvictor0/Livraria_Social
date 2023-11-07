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
    curtidas = models.PositiveIntegerField(default=0)
    data = models.DateField(null=True)
    
    def user_has_liked(self, usuario):
        return CurtidaResenha.objects.filter(usuario=usuario, resenha=self, curtida=True).exists()

    def contagem_curtidas(self):
        return self.curtidas

    #def contagem_comentarios(self):
    #    return self.comentarios.count()

    def curtir(self):
        self.curtidas += 1
        self.save()

    def descurtir(self, usuario):
        curtida = CurtidaResenha.objects.get(usuario=usuario, resenha=self)
        if curtida.curtida:
            self.curtidas -= 1
            self.save()
            curtida.delete()
    
    def __str__(self):
        return f"Comentário sobre {self.livro.nome}"
    
    def data_formatada(self):
        return self.data.strftime('%d de %B %Y')
    
# tabela auxiliar para curtida de resenha
class CurtidaResenha(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    resenha = models.ForeignKey(Resenha, on_delete=models.CASCADE)
    curtida = models.BooleanField(default=True)
 
class Lista_livros(models.Model):
    nome_lista = models.CharField(max_length=100)
    usuario_id = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    livros = models.ManyToManyField('Livros', related_name='livros_salvos')
