from django.shortcuts import render, redirect
from django.conf import settings
from transbank.webpay.webpay_plus.transaction import Transaction
from django.urls import reverse
import requests
from django.http import HttpResponse
import transbank.webpay.webpay_plus as webpay  # Asegúrate de importar webpay correctamente
from ecommerce.models import articulo
from .models import articulo # Ajusta esto según la ubicación de tu modelo Producto
from .carrito import Carrito
# Configurar Webpay Plus según los settings
commerce_code = settings.TRANSACTION_CONFIG['commerce_code']
api_key = settings.TRANSACTION_CONFIG['api_key']
integration_type = settings.TRANSACTION_CONFIG['integration_type']

from django.contrib import messages
from django.contrib.auth import login as auth_login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from .models import articulo, Carritos
from django.http import JsonResponse,HttpResponse
from .forms import ProductosForm
from transbank.webpay.webpay_plus.transaction import Transaction, WebpayOptions
import hashlib
from django.conf import settings
from transbank.common.integration_type import IntegrationType
from django.urls import reverse
import hashlib
from django.shortcuts import redirect, reverse, HttpResponse
import hashlib
from django.shortcuts import redirect, reverse, HttpResponse
from .models import Carritos, articulo
from django.conf import settings
from transbank.webpay.webpay_plus.transaction import Transaction, WebpayOptions
from transbank.common.integration_type import IntegrationType


def iniciar_pago(request):
    if request.method == "POST":
        # Calcular el total del carrito desde la sesión
        total = 0
        if "carrito" in request.session:
            for key, value in request.session["carrito"].items():
                total += int(value["acumulado"])

        if total > 0:
            session_key = request.session.session_key
            buy_order = hashlib.md5(session_key.encode()).hexdigest()[:26]
            session_id = f"sesion_{session_key}"
            amount = total
            return_url = request.build_absolute_uri(reverse('confirmar_pago'))

            tx = Transaction(WebpayOptions(settings.TRANBANK_COMMERCE_CODE, settings.TRANBANK_API_KEY, IntegrationType.TEST))
            try:
                response = tx.create(buy_order, session_id, amount, return_url)
                if response:
                    return redirect(response['url'] + "?token_ws=" + response['token'])
                else:
                    return HttpResponse("No se recibió respuesta de Transbank.")
            except Exception as e:
                return HttpResponse(f"Error interno: {str(e)}")
        else:
            return HttpResponse("El carrito está vacío.")
    else:
        return HttpResponse("Método no permitido.", status=405)

def confirmar_pago(request):
    token_ws = request.GET.get('token_ws')
    if not token_ws:
        return HttpResponse("Token no proporcionado.")

    try:
        tx = Transaction(WebpayOptions(settings.TRANBANK_COMMERCE_CODE, settings.TRANBANK_API_KEY, IntegrationType.TEST))
        response = tx.commit(token_ws)
        if response and response['status'] == 'AUTHORIZED':
            # Obtener el carrito de la sesión
            carrito = request.session.get('carrito', {})
            
            for producto_id, cantidad in carrito.items():
                try:
                    producto = articulo.objects.get(id=producto_id)
                    print(f"Producto: {producto.nombre}, Cantidad: {cantidad}")
                except articulo.DoesNotExist:
                    return HttpResponse(f"Producto con id {producto_id} no encontrado.")

            return render(request, 'ecommerce/pagoconfirmado.html', {'response': response})
        else:
            return render(request, 'ecommerce/pagorechazado.html', {'response': response})
    except Exception as e:
        return HttpResponse(f"Error interno: {str(e)}")



def index(request):
    return render(request, 'ecommerce/index.html')

def carrito(request):
    return render(request, 'ecommerce/carrito.html')

def productos(request):
    productos = articulo.objects.all()
    return render(request, 'ecommerce/productos.html', {'productos': productos})


def agregar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = articulo.objects.get(id=producto_id)
    carrito.agregar(producto)
    return redirect("productos")

def eliminar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = articulo.objects.get(id=producto_id)
    carrito.eliminar(producto)
    return redirect("productos")

def restar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = articulo.objects.get(id=producto_id)
    carrito.restar(producto)
    return redirect("productos")    


def limpiar_carrito(request):
    carrito = Carrito(request)
    carrito.limpiar()
    return redirect("productos")    


def pago(request):
    return render(request, 'ecommerce/pago.html')

def ecommerce(request):
    return render(request, 'ecommerce/ecommerce.html')

def retorno_webpay(request):
    # Aquí puedes manejar la respuesta de retorno de Transbank
    # Por ejemplo, puedes actualizar el estado de la transacción en tu sistema
    # y mostrar un mensaje de confirmación al usuario
    return HttpResponse("¡Pago exitoso! El estado de la transacción ha sido actualizado.")


def login_view(request):
    if request.method == 'GET':
        return render(request, 'ecommerce/login.html', {'form': AuthenticationForm()})
    elif request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('index')
        return render(request, 'ecommerce/login.html', {'form': form, 'error': 'Nombre de usuario o contraseña incorrectos'})  

def logout_view(request):
    logout(request)
    return redirect('index')          


def registro_view(request):
    if request.method == 'GET':
        return render(request, 'ecommerce/registro.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'],
                    password=request.POST['password1']
                )
                user.save()
                auth_login(request, user)  # Autenticar al usuario después de registrarse
                messages.success(request, '¡Te has registrado correctamente!')
                return redirect('index')
            except IntegrityError:
                return render(request, 'registro.html', {
                    'form': UserCreationForm(),
                    'error': 'El usuario ya existe'
                })
        return render(request, 'ecommerce/registro.html', {
            'form': UserCreationForm(),
            'error': 'Las contraseñas no coinciden'
        })

