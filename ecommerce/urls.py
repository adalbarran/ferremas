from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings 

urlpatterns = [
    path('ecommerce', views.ecommerce, name='ecommerce'),
    path('', views.index, name='index'),
    path('productos', views.productos, name='productos'),
    path('pago', views.pago, name='pago'),
    path('carrito', views.carrito, name='carrito'),
    path('detalle/<int:producto_id>/', views.detalles, name='detalles'), 
    path('agregar/<int:producto_id>/', views.agregar_producto, name='agregar_producto'),
    
    path('iniciar-pago/', views.iniciar_pago, name='iniciar_pago'),
    path('retorno-webpay/', views.retorno_webpay, name='retorno_webpay'),
    path('registro/', views.registro_view, name='registro'),

    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('pagos/confirmar/', views.confirmar_pago, name='confirmar_pago')


]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
