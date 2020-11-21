# Django
from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic

# Modelos
from pacientes.models import Paciente

# Formularios
from .forms import FiltroPacientes

# Utils
from .utils import generar_reporte_pdf

# 1 - Todos
# 2 - Pacientes que asistieron a los turnos en la semana
# 3 - Pacientes que asistieron a los turnos en la mes
# 4 - Pacientes que no asistieron a los turnos en la semana
# 5 - Pacientes que no asistieron a los turnos en la mes
# 6 - Pacientes que hicieron por lo menos un pedido en la semana
# 7 - Pacientes que hicieron por lo menos un pedido en la mes
# 8 - Ventas totales por mes, clasificadas por vendedores.
# 9 - Todos

class ListaPacientes(generic.ListView):
    """ Vista para generar reportes de pacientes. """
    context_object_name = 'pacientes'
    template_name = 'clinica/reportes/pacientes.html'

    def get_queryset(self):
        filtros = self.request.GET.get('filtros')
        breakpoint()
        return Paciente.objects.all()

    """
    def get(self, request, *args, **kwargs):
        
        ctx = {
            'pacientes': self.queryset
        }
        pdf = generar_reporte_pdf(self.template_name, ctx)
        return HttpResponse(pdf, content_type='application/pdf')"""

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['form'] = FiltroPacientes
        contexto['titulo'] = 'Pacientes'
        return contexto 