from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('valida_cadastro/', views.valida_cadastro, name= 'valida_cadastro'),
    path('confirmar_email/<int:user_id>/<str:token>/', views.confirmar_email, name='confirmar_email'),
    

]
