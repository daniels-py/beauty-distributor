from django.shortcuts import render
from django.db import DatabaseError
from django.forms import ValidationError
from django.views import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from beauty_distributor.models import *
import json
from django.db.models import Q
# Create your views here.



def Portada(request):
    return render(request, "index.html")




@method_decorator(csrf_exempt, name='dispatch')
class ListarCategorias(View):   
    def get(self, request):
        try:
            nombre = request.GET.get('nombre')
            categorias = Categoria.objects.all()

            if nombre:
                categorias = categorias.filter(nombre__icontains=nombre)

            # Validación del número de página
            try:
                page_number = int(request.GET.get('page', 1))
            except (ValueError, TypeError):
                page_number = 1

            try:
                page_size = min(int(request.GET.get('page_size', 10)), 100)  # Límite de 100 por página
            except (ValueError, TypeError):
                page_size = 10  # Valor predeterminado si hay un error en la paginación

            paginator = Paginator(categorias, page_size)
            page_obj = paginator.get_page(page_number)

            datos_categorias = [
                {
                    'id': categoria.id,
                    'nombre': categoria.nombre,
                    'descripcion': categoria.descripcion,
                    'permite_color': categoria.permite_color  # Agregado para mostrar si permite carta de colores
                }
                for categoria in page_obj
            ]

            if not datos_categorias:
                return JsonResponse({'categorias': []}, status=200)  # Cambia a un objeto JSON con una lista vacía

            return JsonResponse({
                'categorias': datos_categorias,
                'page': page_obj.number,
                'pages': paginator.num_pages,
                'total': paginator.count
            })

        except DatabaseError as db_err:
            return JsonResponse({'error': 'Error en la base de datos: ' + str(db_err)}, status=500)
        except Exception as e:
            return JsonResponse({'error': 'Error interno: ' + str(e)}, status=500)

    def get(self, request):
        try:
            nombre = request.GET.get('nombre')
            categorias = Categoria.objects.all()

            if nombre:
                categorias = categorias.filter(nombre__icontains=nombre)

            # Validación del número de página
            try:
                page_number = int(request.GET.get('page', 1))
            except (ValueError, TypeError):
                page_number = 1

            try:
                page_size = min(int(request.GET.get('page_size', 10)), 100)  # Límite de 100 por página
            except (ValueError, TypeError):
                page_size = 10  # Valor predeterminado si hay un error en la paginación

            paginator = Paginator(categorias, page_size)
            page_obj = paginator.get_page(page_number)

            datos_categorias = [
                {
                    'id': categoria.id,
                    'nombre': categoria.nombre,
                    'descripcion': categoria.descripcion,
                    'permite_color': categoria.permite_color  # Agregado para mostrar si permite carta de colores
                }
                for categoria in page_obj
            ]

            if not datos_categorias:
                return JsonResponse({'message': 'No hay categorías disponibles'}, status=404)

            return JsonResponse({
                'categorias': datos_categorias,
                'page': page_obj.number,
                'pages': paginator.num_pages,
                'total': paginator.count
            })

        except DatabaseError as db_err:
            return JsonResponse({'error': 'Error en la base de datos: ' + str(db_err)}, status=500)
        except Exception as e:
            return JsonResponse({'error': 'Error interno: ' + str(e)}, status=500)