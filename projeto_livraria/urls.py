from django.contrib import admin
from django.urls import path,include
from usuarios.views import login

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login, name='login'),
    path('livro/', include('livro.urls')),
    path('auth/', include('usuarios.urls'))
]
