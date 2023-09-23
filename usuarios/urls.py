from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('valida_cadastro/', views.valida_cadastro, name= 'valida_cadastro'),
    path('valida_login/', views.valida_login, name= 'valida_login'),
    path('sair/', views.sair, name= 'sair'),
    path('solicitar_redefinicao_senha/', views.solicitar_redefinicao_senha, name='solicitar_redefinicao_senha'),
    path('redefinir_senha/<str:token>/', views.redefinir_senha, name='redefinir_senha'),
    path('confirmar_email/<int:user_id>/<str:token>/', views.confirmar_email, name='confirmar_email'),
]