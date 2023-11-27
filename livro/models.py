from django.db import models
from usuarios.models import Usuario

class Livros(models.Model):
    isbn = models.TextField(primary_key=True, unique=True)
    nome = models.CharField()
    autor = models.CharField()
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
    comentarios = models.ManyToManyField('Comentarios_Resenha', related_name='comentario_resenha')
    curtidas = models.PositiveIntegerField(default=0)
    data = models.DateField(null=True)
    melhor_resenha = models.IntegerField(default=0)
    data_atual = models.DateField(null=True)
    data_final = models.DateField(null=True)

    class Meta:
        db_table = 'Resenha'
    
    def user_has_liked(self, usuario):
        return CurtidaResenha.objects.filter(usuario=usuario, resenha=self, curtida=True).exists()

    def contagem_curtidas(self):
        return self.curtidas

    def contagem_comentarios(self):
        return self.comentarios.count()

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

    class Meta:
        db_table = 'CurtidaResenha'
 
class Lista_livros(models.Model):
    nome_lista = models.CharField(max_length=100)
    usuario_id = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    livros = models.ManyToManyField('Livros', related_name='livros_salvos')
    
    class Meta:
        db_table = 'Lista_livros'

class Comentarios_Resenha(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    resenha_id = models.ForeignKey(Resenha, on_delete=models.CASCADE)
    texto = models.TextField()
    data = models.DateField(null=True)

    class Meta:
        db_table = 'Comentarios_Resenha'

    def data_formatada(self):
        return self.data.strftime('%d de %B %Y')
    