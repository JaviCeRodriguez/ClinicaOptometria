# Django
from django.urls import path

# Vistas
from .views import ListaPacientes, descargarPDF

app_name = 'reportes'

urlpatterns = [
    path('pacientes/',ListaPacientes.as_view(), name='pacientes'),
    path('descargar/', descargarPDF, name='descargar')
]