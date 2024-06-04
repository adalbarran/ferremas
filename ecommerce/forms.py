from django import forms
from .models import articulo

class ProductosForm(forms.ModelForm):
    class Meta:
        model = articulo
        fields = '__all__' 
