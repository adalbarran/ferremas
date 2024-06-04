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



def iniciar_pago(request):
    # Datos de la transacción
    amount = 10000  # Monto en pesos chilenos
    buy_order = '123'
    session_id = '1'
    return_url = request.build_absolute_uri(reverse('retorno_webpay'))  # Obtener la URL de retorno absoluta
    
    # Crear la transacción utilizando el SDK de Transbank
    resp = webpay.create(buy_order, session_id, amount, return_url)
    
    # Manejar la respuesta
    if resp["response_code"] == "SUCCESS":
        url = resp['url']
        token = resp['token']
        redirect_url = resp.get("url")
        return render(request, 'pago.html', {'redirect_url': redirect_url})
    else:
        return HttpResponse("Error al crear la transacción con Transbank")



def index(request):
    return render(request, 'ecommerce/index.html')

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