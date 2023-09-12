from django.db import models

class Usuario(models.Model):
    nome = models.CharField(max_length=50)
    email = models.EmailField()
    senha = models.CharField(max_length=64)
    #token de redefinição de senha
    token_confirmacao = models.CharField(max_length=100, null=True, blank=True)
    data_expiracao_token = models.DateTimeField(null=True, blank=True)
    # Campo de confirmação de email
    confirmado = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.nome