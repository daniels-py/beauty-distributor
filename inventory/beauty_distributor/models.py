from django.core.exceptions import ValidationError
from django.db import models

# Modelo para representar categorías de productos
class Categoria(models.Model):
    nombre = models.CharField(max_length=255, verbose_name='Nombre de la Categoría')
    descripcion = models.TextField(verbose_name='Descripción de la Categoría')
    
    # Método para permitir categorías que gestionen productos con color
    permite_color = models.BooleanField(default=False, verbose_name='¿Permite Carta de Colores?')

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'


# Modelo para representar marcas de productos
class Marca(models.Model):
    nombre = models.CharField(max_length=255, verbose_name='Nombre de la Marca')

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Marca'
        verbose_name_plural = 'Marcas'


# Modelo para representar presentaciones de productos
class Presentacion(models.Model):
    nombre = models.CharField(max_length=255, verbose_name='Nombre de la Presentación')
    descripcion = models.TextField(verbose_name='Descripción de la Presentación')

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Presentación'
        verbose_name_plural = 'Presentaciones'


# Modelo para representar cartas de color específicas por marca
class CartaColor(models.Model):
    codigo_color = models.CharField(max_length=50, verbose_name='Código de Color')
    nombre_color = models.CharField(max_length=255, verbose_name='Nombre del Color')
    hexadecimal = models.CharField(max_length=7, verbose_name='Código Hexadecimal')
    descripcion = models.TextField(verbose_name='Descripción del Color', blank=True)

    # Ajustar el campo `marca` con una función predeterminada
    def default_marca():
        try:
            return Marca.objects.first()  # Asigna la primera marca existente en la base de datos
        except Marca.DoesNotExist:
            return None  # O lanzar un error si prefieres asegurar que siempre haya una marca
    
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE, related_name='cartas_colores', default=default_marca)

    def __str__(self):
        return f'{self.nombre_color} ({self.codigo_color}) - {self.marca.nombre}'

    class Meta:
        verbose_name = 'Carta de Color'
        verbose_name_plural = 'Cartas de Colores'
        unique_together = ('codigo_color', 'marca')


# Modelo para representar productos
class Producto(models.Model):
    nombre = models.CharField(max_length=255, verbose_name='Nombre del Producto')
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE, related_name='productos')
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='productos')
    presentacion = models.ForeignKey(Presentacion, on_delete=models.CASCADE, related_name='productos')
    descripcion = models.TextField(verbose_name='Descripción del Producto', default="Descripción no disponible")
    carta_color = models.ForeignKey(CartaColor, on_delete=models.SET_NULL, null=True, blank=True, related_name='productos', verbose_name='Carta de Color')

    def __str__(self):
        return f'{self.nombre} - {self.marca.nombre}'

    # Validación para productos que no deben tener carta de color
    def clean(self):
        if self.carta_color and not self.categoria.permite_color:
            raise ValidationError('Este producto no debería tener carta de color asociada, ya que la categoría no lo permite.')

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'


# Modelo para representar el inventario de productos
class Inventario(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='inventario')
    unidades = models.PositiveIntegerField(default=0, verbose_name='Unidades')

    def __str__(self):
        return f'{self.producto.nombre} - {self.unidades} unidades'

    class Meta:
        verbose_name = 'Inventario'
        verbose_name_plural = 'Inventarios'
        unique_together = ('producto',)
