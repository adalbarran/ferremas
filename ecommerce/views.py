import hashlib
import json
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth import login as auth_login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from transbank.webpay.webpay_plus.transaction import Transaction, WebpayOptions
from transbank.common.integration_type import IntegrationType
from ecommerce.models import articulo
from .carrito import Carrito
from .utils import obtener_tipo_cambio, SERIES_CODIGOS
from ecommerce.templatetags.custom_filters import formato_moneda
from decimal import Decimal
import requests
from django.http import JsonResponse
from django.conf import settings
from ecommerce.templatetags.custom_filters import formato_moneda
from .utils import obtener_tipo_cambio, SERIES_CODIGOS
def iniciar_pago(request):
    if request.method == "POST":
        total = sum(int(value["acumulado"]) for value in request.session.get("carrito", {}).values())
        
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
    carrito = request.session.get('carrito', {})
    total_carrito = Decimal(0)
    for key, value in carrito.items():
        producto = articulo.objects.get(id=value['producto_id'])
        value['image_url'] = producto.imagen.url if producto.imagen else None
        total_carrito += Decimal(value['acumulado'])

    context = {
        'carrito': carrito,
        'total_carrito': total_carrito,
    }
    return render(request, 'ecommerce/carrito.html', context)

def productos(request):
    productos = articulo.objects.all()
    return render(request, 'ecommerce/productos.html', {'productos': productos})

@require_POST
def agregar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = get_object_or_404(articulo, id=producto_id)
    carrito.agregar(producto)
    return redirect('carrito')

@require_POST
def restar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = get_object_or_404(articulo, id=producto_id)
    carrito.restar(producto)
    return redirect('carrito')

def eliminar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = articulo.objects.get(id=producto_id)
    carrito.eliminar(producto)
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
                auth_login(request, user)
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

def detalles(request, producto_id):
    producto = get_object_or_404(articulo, id=producto_id)

    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = json.loads(request.body)
        moneda = data.get('moneda', 'CLP')
    else:
        moneda = 'CLP'

    serie_codigo = SERIES_CODIGOS.get(moneda)
    tipo_cambio = obtener_tipo_cambio(serie_codigo)

    if tipo_cambio != Decimal('1'):
        precio_convertido = producto.precio / tipo_cambio
    else:
        precio_convertido = producto.precio

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = {
            'precio_convertido': formato_moneda(precio_convertido, moneda),
            'tipo_cambio': formato_moneda(tipo_cambio, 'CLP') if tipo_cambio != Decimal('1') else None,
            'moneda': moneda
        }
        return JsonResponse(data)

    context = {
        'producto': producto,
        'moneda': moneda,
        'precio_convertido': precio_convertido,
        'tipo_cambio': tipo_cambio
    }

    return render(request, 'ecommerce/productos.html', context)

def convertir_moneda(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = json.loads(request.body)
        moneda = data.get('moneda', 'CLP')

        # Obtener el tipo de cambio desde la API del Banco Central
        serie_codigo = SERIES_CODIGOS.get(moneda)
        tipo_cambio = obtener_tipo_cambio(serie_codigo)

        # Calcular el total del carrito en la moneda especificada
        total_carrito = Decimal(0)
        if "carrito" in request.session:
            for key, value in request.session["carrito"].items():
                precio_producto = Decimal(value.get('acumulado', 0))
                total_carrito += precio_producto / tipo_cambio

        # Formatear el total del carrito en la moneda especificada
        total_carrito_formato = formato_moneda(total_carrito, moneda)

        # Preparar la respuesta JSON
        data = {
            'precio_convertido': total_carrito_formato,
            'tipo_cambio': formato_moneda(tipo_cambio, 'CLP') if tipo_cambio != Decimal('1') else None,
            'moneda': moneda,
        }
        return JsonResponse(data)
    return JsonResponse({}, status=400)