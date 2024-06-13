from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class articulo(models.Model):
    nombre = models.CharField(max_length=100, blank=False, null=False)
    categoria = models.CharField(max_length=32)
    precio = models.IntegerField()
    imagen = models.ImageField(upload_to='imagenes_articulos/', blank=True, null=True)
    def __str__(self):
        return f'{self.nombre} -> {self.precio}'

class Carritos(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    articulos = models.ManyToManyField('articulo', related_name='carritos', blank=True)

    def __str__(self):
        return f"Carrito de {self.usuario.username}"

