from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings 

urlpatterns = [
    path('ecommerce', views.ecommerce, name='ecommerce'),
    path('', views.index, name='index'),
    path('productos', views.productos, name='productos'),
    path('pago', views.pago, name='pago'),

    path('iniciar-pago/', views.iniciar_pago, name='iniciar_pago'),
    path('retorno-webpay/', views.retorno_webpay, name='retorno_webpay'),


]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
