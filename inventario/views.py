from django.shortcuts import render, get_object_or_404, redirect
from .models import Producto
from django.http import HttpResponse
from django.contrib import messages
from .forms import ProductoForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test

def iniciar_sesion(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('lista_productos')  # Redirige al usuario a la página de productos
    else:
        form = AuthenticationForm()
    return render(request, 'iniciar_sesion.html', {'form': form})

@login_required
def registrar(request):
    if not request.user.is_superuser:
        return redirect('login')  # Si el usuario no es admin, redirige al login
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirige a la página de inicio de sesión después del registro
    else:
        form = UserCreationForm()
    return render(request, 'registrar.html', {'form': form})

# Esta vista solo será accesible por el superusuario
@user_passes_test(lambda u: u.is_superuser)
def crear_usuario(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_productos')  # Redirige a la lista de productos después de crear el usuario
    else:
        form = UserCreationForm()
    return render(request, 'crear_usuario.html', {'form': form})


def cerrar_sesion(request):
    logout(request)
    return redirect('login')  # Redirige a la página de inicio de sesión después de cerrar sesión

# Vista para listar productos
@login_required
def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'inventario/lista_productos.html', {'productos': productos})

# Vista para agregar un producto
def agregar_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lista_productos')
    else:
        form = ProductoForm()
    return render(request, 'inventario/agregar_producto.html', {'form': form})

# Vista para editar un producto
def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)

    if request.method == 'POST':
        # Obtener los valores del formulario
        nombre = request.POST['nombre']
        descripcion = request.POST['descripcion']
        precio = request.POST['precio']
        cantidad = request.POST['cantidad']
        imagen = request.FILES.get('imagen')

        # Actualizar el producto
        producto.nombre = nombre
        producto.descripcion = descripcion
        producto.precio = precio
        producto.cantidad = cantidad
        if imagen:
            producto.imagen = imagen
        producto.save()

        # Mostrar mensaje de éxito
        messages.success(request, 'Producto editado correctamente')

        # Redirigir a la lista de productos
        return redirect('lista_productos')

    return render(request, 'inventario/editar_producto.html', {'producto': producto})

# Vista para eliminar un producto
def eliminar_producto(request, pk):
    # Obtener el producto con la clave primaria pk
    producto = get_object_or_404(Producto, pk=pk)
    
    # Eliminar el producto
    producto.delete()
    
    # Redirigir a la lista de productos
    return redirect('lista_productos')
