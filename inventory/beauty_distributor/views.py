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


def Home(request):
    return render(request, "home.html")



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
            page_number = self._get_page_number(request)
            page_size = self._get_page_size(request)

            paginator = Paginator(categorias, page_size)
            page_obj = paginator.get_page(page_number)

            datos_categorias = [
                {
                    'id': categoria.id,
                    'nombre': categoria.nombre,
                    'descripcion': categoria.descripcion,
                    'permite_color': categoria.permite_color
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

    def _get_page_number(self, request):
        try:
            return int(request.GET.get('page', 1))
        except (ValueError, TypeError):
            return 1

    def _get_page_size(self, request):
        try:
            return min(int(request.GET.get('page_size', 10)), 100)  # Límite de 100 por página
        except (ValueError, TypeError):
            return 10  # Valor predeterminado

@method_decorator(csrf_exempt, name='dispatch')
class CrearCategoria(View):
    def post(self, request):
        return self.crear_categoria(request)

    def crear_categoria(self, request):
        try:
            data = json.loads(request.body)
            nueva_categoria = Categoria.objects.create(
                nombre=data['nombre'],
                descripcion=data['descripcion'],
                permite_color=data.get('permite_color', False)  # Default a False si no se proporciona
            )
            return JsonResponse({'id': nueva_categoria.id, 'nombre': nueva_categoria.nombre, 'descripcion': nueva_categoria.descripcion}, status=201)
        except (KeyError, ValueError) as e:
            return JsonResponse({'error': str(e)}, status=400)
        except DatabaseError:
            return JsonResponse({'error': 'Error al crear la categoría'}, status=500)
        except ValidationError as e:
            return JsonResponse({'error': e.messages}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class ListarMarcas(View):
    def get(self, request):
        try:
            marcas = Marca.objects.all()

            datos_marcas = [
                {
                    'id': marca.id,
                    'nombre': marca.nombre,
                    'productos_count': marca.productos.count()
                }
                for marca in marcas
            ]

            if not datos_marcas:
                return JsonResponse({'message': 'Marcas no disponibles.'}, status=404)

            return JsonResponse(datos_marcas, safe=False, status=200)

        except DatabaseError:
            return JsonResponse({'error': 'Error al obtener las marcas.'}, status=500)

@method_decorator(csrf_exempt, name='dispatch')
class CrearMarca(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            nombre = data.get('nombre')

            if not nombre:
                return JsonResponse({'error': 'El nombre es obligatorio.'}, status=400)

            marca = Marca(nombre=nombre)
            marca.save()
            return JsonResponse({'message': 'Marca creada con éxito.', 'id': marca.id}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Datos inválidos.'}, status=400)
        except DatabaseError:
            return JsonResponse({'error': 'Error al crear la marca.'}, status=500)

@method_decorator(csrf_exempt, name='dispatch')
class ListarPresentaciones(View):
    def get(self, request):
        try:
            presentaciones = Presentacion.objects.all()

            datos_presentaciones = [
                {
                    'id': presentacion.id,
                    'nombre': presentacion.nombre,
                    'productos_asociados_count': presentacion.productos.count()
                }
                for presentacion in presentaciones
            ]

            if not datos_presentaciones:
                return JsonResponse({'mensaje': 'Presentaciones no disponibles'}, status=404)

            return JsonResponse(datos_presentaciones, safe=False, status=200)

        except DatabaseError:
            return JsonResponse({'error': 'Error al obtener las presentaciones'}, status=500)

@method_decorator(csrf_exempt, name='dispatch')
class CrearPresentacion(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            nombre = data.get('nombre')
            if not nombre:
                return JsonResponse({'error': 'El nombre es obligatorio'}, status=400)

            presentacion = Presentacion.objects.create(nombre=nombre)
            return JsonResponse({'id': presentacion.id, 'nombre': presentacion.nombre}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Datos inválidos'}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class ListarCartasColor(View):
    def get(self, request):
        try:
            # Obtener todas las cartas de color junto con las marcas relacionadas
            cartas_color = CartaColor.objects.select_related('marca').all()

            # Crear un diccionario para agrupar las cartas de color por marca
            cartas_por_marca = {}
            for cc in cartas_color:
                marca_nombre = cc.marca.nombre
                if marca_nombre not in cartas_por_marca:
                    cartas_por_marca[marca_nombre] = []
                cartas_por_marca[marca_nombre].append({
                    'id': cc.id,
                    'nombre_color': cc.nombre_color,
                    'codigo_color': cc.codigo_color,
                    'hexadecimal': cc.hexadecimal,
                    'descripcion': cc.descripcion
                })

            # Convertir el diccionario en una lista de marcas con sus cartas
            cartas_de_color = [
                {
                    'marca': marca,
                    'cartas': cartas
                }
                for marca, cartas in cartas_por_marca.items()
            ]

            # Si no hay datos, devolver un mensaje
            if not cartas_de_color:
                return JsonResponse({'mensaje': 'Cartas de color no disponibles'}, status=404)

            # Devolver el JSON con la estructura deseada
            return JsonResponse({'cartas_de_color': cartas_de_color}, safe=False, status=200)

        except DatabaseError:
            return JsonResponse({'error': 'Error al obtener las cartas de color'}, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class CrearCartaColor(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            nombre = data.get('nombre')
            marca_id = data.get('marca_id')

            if not nombre or not marca_id:
                return JsonResponse({'error': 'El nombre y la marca son obligatorios'}, status=400)

            carta_color = CartaColor.objects.create(nombre=nombre, marca_id=marca_id)
            return JsonResponse({'id': carta_color.id, 'nombre': carta_color.nombre, 'marca_id': carta_color.marca.id}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Datos inválidos'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class ListarProductos(View):
    def get(self, request):
        productos = Producto.objects.all()
        if not productos:
            return JsonResponse({'mensaje': 'Productos no disponibles'}, status=404)

        data = [{'id': p.id, 'nombre': p.nombre, 'categoria': p.categoria.nombre, 'marca': p.marca.nombre} for p in productos]
        return JsonResponse(data, safe=False, status=200)

@method_decorator(csrf_exempt, name='dispatch')
class CrearProducto(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            nombre = data.get('nombre')
            categoria_id = data.get('categoria_id')
            marca_id = data.get('marca_id')
            presentacion_id = data.get('presentacion_id')
            carta_color_id = data.get('carta_color_id')

            if not nombre or not categoria_id or not marca_id or not presentacion_id:
                return JsonResponse({'error': 'El nombre, categoría, marca y presentación son obligatorios'}, status=400)

            producto = Producto.objects.create(
                nombre=nombre,
                categoria_id=categoria_id,
                marca_id=marca_id,
                presentacion_id=presentacion_id,
                carta_color_id=carta_color_id  # Se puede dejar como None si no se proporciona
            )
            return JsonResponse({
                'id': producto.id,
                'nombre': producto.nombre,
                'categoria_id': producto.categoria.id,
                'marca_id': producto.marca.id,
                'presentacion_id': producto.presentacion.id
            }, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Datos inválidos'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class ListarInventario(View):
    def get(self, request):
        try:
            inventarios = Inventario.objects.select_related('producto').all()
            if not inventarios:
                return JsonResponse({'mensaje': 'Inventario no disponible'}, status=404)

            data = [
                {
                    'id': inv.id,
                    'producto': inv.producto.nombre,
                    'categoria': inv.producto.categoria.nombre,
                    'marca': inv.producto.marca.nombre,
                    'unidades': inv.unidades
                }
                for inv in inventarios
            ]

            return JsonResponse(data, safe=False, status=200)

        except DatabaseError:
            return JsonResponse({'error': 'Error al obtener el inventario'}, status=500)

@method_decorator(csrf_exempt, name='dispatch')
class CrearInventario(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            producto_id = data.get('producto_id')
            unidades = data.get('unidades', 0)

            if not producto_id:
                return JsonResponse({'error': 'El ID del producto es obligatorio.'}, status=400)

            try:
                producto = Producto.objects.get(id=producto_id)
            except Producto.DoesNotExist:
                return JsonResponse({'error': 'El producto no existe.'}, status=404)

            inventario, creado = Inventario.objects.get_or_create(producto=producto)
            inventario.unidades = unidades
            inventario.save()

            mensaje = 'Producto añadido al inventario.' if creado else 'Inventario actualizado.'
            return JsonResponse({'message': mensaje, 'producto_id': producto.id, 'unidades': inventario.unidades}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Datos inválidos.'}, status=400)
        except DatabaseError:
            return JsonResponse({'error': 'Error al crear o actualizar el inventario.'}, status=500)