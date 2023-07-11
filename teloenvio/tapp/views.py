import random
import string
from django.core.mail import send_mail
from django.shortcuts import render,  get_object_or_404
from .models import Producto, Pedido
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from .forms import CustomRegistroForm


# Create your views here.

def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'productos/lista.html', {'productos': productos})

def ingreso_pedidos(request):
    if request.method == 'POST':
        # Obtener los datos del formulario
        cliente = request.POST.get('cliente')
        direccion_entrega = request.POST.get('direccion_entrega')
        productos = request.POST.getlist('productos')
        cantidades = request.POST.get('cantidades')
        precio_total = request.POST.get('precio_total')
        forma_pago = request.POST.get('forma_pago')

        # Crear el objeto Pedido
        pedido = Pedido.objects.create(cliente=cliente, direccion_entrega=direccion_entrega, cantidades=cantidades, precio_total=precio_total, forma_pago=forma_pago)

        # Asociar los productos al pedido
        pedido.productos.set(productos)

        # Redirigir a la página de éxito o realizar otras acciones necesarias

    else:
        # Renderizar el formulario de ingreso de pedidos
        return render(request, 'ingreso_pedidos.html')

def lista_pedidos(request):
    pedidos = Pedido.objects.all()
    return render(request, 'lista_pedidos.html', {'pedidos': pedidos})

def actualizar_estado_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, pk=pedido_id)

    if request.method == 'POST':
        nuevo_estado = request.POST.get('estado')
        pedido.estado = nuevo_estado
        pedido.save()
        

# class RegistroUsuarioView(CreateView):
#     template_name = 'registro.html'
#     form_class = UserCreationForm
#     success_url = reverse_lazy('login')

class RegistroUsuarioView(CreateView):
    template_name = 'registro.html'
    form_class = CustomRegistroForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        # Generar una contraseña aleatoria
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        # Actualizar la contraseña del usuario registrado
        user = self.object
        user.set_password(password)
        user.save()
        # Enviar la contraseña aleatoria por correo electrónico
        send_mail(
            'Confirmación de registro',
            f'Hola {user.username}, tu contraseña aleatoria es: {password}',
            'noreply@example.com',
            [user.email],
            fail_silently=False,
        )
        return response


def realizar_pedido(request):
    if request.method == 'POST':
        # Obtener los datos del formulario
        direccion_entrega = request.POST.get('direccion_entrega')
        productos_ids = request.POST.getlist('productos')
        cantidades = request.POST.getlist('cantidades')
        forma_pago = request.POST.get('forma_pago')

        # Obtener los productos seleccionados
        productos = Producto.objects.filter(id__in=productos_ids)

        # Calcular el precio total del pedido
        precio_total = sum(producto.precioProducto * int(cantidad) for producto, cantidad in zip(productos, cantidades))

        # Crear el objeto Pedido
        pedido = Pedido.objects.create(direccion_entrega=direccion_entrega, precio_total=precio_total, forma_pago=forma_pago)

        # Asociar los productos al pedido con las cantidades correspondientes
        for producto, cantidad in zip(productos, cantidades):
            pedido.productos.add(producto, through_defaults={'cantidad': cantidad})

        return redirect('pedido_exitoso')
    else:
        productos_disponibles = Producto.objects.all()

        return render(request, 'realizar_pedido.html', {'productos': productos_disponibles})
    

def historial_pedidos(request):
    pedidos = Pedido.objects.filter(cliente=request.user)

    return render(request, 'historial_pedidos.html', {'pedidos': pedidos})

def cancelar_pedido(request, numero_pedido):
    pedido = get_object_or_404(Pedido, numero_pedido=numero_pedido)

    # Verificar si el pedido se encuentra en los estados "pendiente" o "en preparación"
    if pedido.estado in ['P', 'PR']:
        # Cancelar el pedido
        pedido.delete()

    return redirect('historial_pedidos')

def pedidos_microempresario(request):
    pedidos = Pedido.objects.filter(productor=request.user.productor)

    return render(request, 'pedidos_microempresario.html', {'pedidos': pedidos})

def inicio(request):
    return render(request, 'inicio.html')