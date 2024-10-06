from django.urls import path
from django.http import HttpResponse
from .views import *


urlpatterns = [
    
        path('Principal/', Portada, name="Principal"),

          
        # Categorías
        path('categorias/', ListarCategorias.as_view(), name='listar_categorias'),
 
]
