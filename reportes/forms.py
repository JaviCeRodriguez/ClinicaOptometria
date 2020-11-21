# Django
from django import forms
from django.db.models import Q

# Modelos
from .models import Filtro

class FiltroPacientes(forms.Form):
    filtros = forms.ModelChoiceField(queryset=Filtro.objects.filter(
        Q(recurso='Pacientes')|Q(recurso='Todos')), label=''
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['filtros'].widget.attrs['class'] = 'form-control mt-2 rounded' 

    class Meta:
        fields = ['filtros']