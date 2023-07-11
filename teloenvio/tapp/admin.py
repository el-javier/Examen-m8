from django.contrib import admin
from .models import Producto, Pedido, Cliente

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('idProductor', 'descripcionProducto', 'precioProducto', 'imagenProducto', 'stockProducto')
    list_filter = ('idProductor',)

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    pass

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    pass
