from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login/', views.login, name='login'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('valida_cadastro/', views.valida_cadastro, name= 'valida_cadastro'),
    path('valida_login/', views.valida_login, name= 'valida_login'),
    path('sair/', views.sair, name= 'sair'),
    path('solicitar_redefinicao_senha/', views.solicitar_redefinicao_senha, name='solicitar_redefinicao_senha'),
    path('redefinir_senha/<str:token>/', views.redefinir_senha, name='redefinir_senha'),
    path('confirmar_email/<int:user_id>/<str:token>/', views.confirmar_email, name='confirmar_email'),
    
    path('perfil/', views.perfil, name='perfil'),
    path('deletar_conta/<int:id>/', views.deletar_conta, name='deletar_conta'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)