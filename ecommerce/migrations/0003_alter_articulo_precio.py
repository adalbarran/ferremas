# Generated by Django 4.2.2 on 2024-06-04 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0002_articulo_carrito_delete_producto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articulo',
            name='precio',
            field=models.IntegerField(),
        ),
    ]