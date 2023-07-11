from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django import forms


class Productor(models.Model):
    nombreContacto = models.CharField(max_length=100)
    RUT = models.CharField(max_length=12)
    razonSocial = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255)
    comuna = models.CharField(max_length=100)
    rubro = models.CharField(max_length=100)

    def __str__(self):
        return self.nombreContacto
    

class Producto(models.Model):
    idProductor = models.ForeignKey('Productor', on_delete=models.CASCADE)
    descripcionProducto = models.CharField(max_length=255)
    precioProducto = models.DecimalField(max_digits=8, decimal_places=2)
    imagenProducto = models.ImageField(upload_to='productos/')
    stockProducto = models.IntegerField()

    def __str__(self):
        return self.descripcionProducto
    

class Cliente(models.Model):
    fono = models.CharField(max_length=15)
    correo = models.EmailField()
    nombre = models.CharField(max_length=100)
    identificador = models.CharField(max_length=20)
    numIdentificador = models.CharField(max_length=50)

# class Pedido(models.Model):
#     numero_pedido = models.AutoField(primary_key=True)  #para generar el número único
#     cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE)
#     direccion_entrega = models.CharField(max_length=255)
#     productos = models.ManyToManyField('Producto')
#     cantidades = models.CharField(max_length=255)
#     precio_total = models.DecimalField(max_digits=8, decimal_places=2)
#     forma_pago = models.CharField(max_length=100)

#     def __str__(self):
#         return f'Pedido {self.numero_pedido}'

class Pedido(models.Model):
    ESTADO_CHOICES = (
        ('P', 'Pendiente'),
        ('PR', 'En preparación'),
        ('D', 'En despacho'),
        ('E', 'Entregado'),
    )

    numero_pedido = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    direccion_entrega = models.CharField(max_length=255)
    productos = models.ManyToManyField(Producto, through='DetallePedido')
    cantidades = models.CharField(max_length=255)
    precio_total = models.DecimalField(max_digits=8, decimal_places=2)
    forma_pago = models.CharField(max_length=100)
    estado = models.CharField(max_length=2, choices=ESTADO_CHOICES, default='P')

    def __str__(self):
        return f'Pedido {self.numero_pedido}'


class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    cantidad = models.IntegerField()

