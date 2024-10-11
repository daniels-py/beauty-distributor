from django.urls import path
from django.http import HttpResponse
from .views import *


urlpatterns = [
        
        # Vistas por defecto
        path('Home/', Home, name="Home"),
        path('Principal/', Portada, name="Principal"),

        # Categorías
        path('categorias/', ListarCategorias.as_view(), name='listar_categorias'),
        path('categorias/crear/', CrearCategoria.as_view(), name='crear_categoria'),

        # Marcas
        path('marcas/', ListarMarcas.as_view(), name='listar_marcas'),  
        path('marcas/crear/', CrearMarca.as_view(), name='crear_marca'),  

        # Presentaciones
        path('presentaciones/', ListarPresentaciones.as_view(), name='listar_presentaciones'),  
        path('presentaciones/crear/', CrearPresentacion.as_view(), name='crear_presentacion'),

        # Carta de color
        path('cartas-color/', ListarCartasColor.as_view(), name='listar_cartas_color'),  
        path('cartas-color/crear/', CrearCartaColor.as_view(), name='crear_carta_color'),

        # Productos
        path('productos/', ListarProductos.as_view(), name='listar_productos'), 
        path('productos/crear/', CrearProducto.as_view(), name='crear_producto'),  

        # Inventario
        path('inventario/', ListarInventario.as_view(), name='listar_inventario'),
        path('inventario/crear/', CrearInventario.as_view(), name='crear_inventario'),

]
