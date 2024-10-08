from django.urls import path
from django.http import HttpResponse
from .views import *


urlpatterns = [
        
        # Vistas por defecto
        path('Home/', Home, name="Home"),
        path('Principal/', Portada, name="Principal"),

        # Categorías
        path('categorias/', ListarCategorias.as_view(), name='listar_categorias'),
 
]
