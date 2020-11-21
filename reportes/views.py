# Django
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy
from django.shortcuts import render
from django.utils import timezone
from django.views import generic
from django.db.models import Q

# Modelos
from pacientes.models import Paciente, Turno
from productos.models import Pedido
from .models import Filtro

# Formularios
from .forms import FiltroPacientes

# Utils
from .utils import generar_reporte_pdf

# Todos
# Pacientes que asistieron a los turnos en la semana/mes LISTO
# Pacientes que no asistieron a los turnos en la semana/mes LISTO
# Pacientes que hicieron por lo menos un pedido en la semana/mes LISTO
# Ventas totales por mes, clasificadas por vendedores.

pacientes = []
query_reporte = 'Pacientes'

def todosLosPacientes():
    pacientes.clear()
    for p in Paciente.objects.all():
            pacientes.append(p)

class ListaPacientes(generic.ListView):
    """ Vista para generar reportes de pacientes. """
    context_object_name = 'pacientes'
    template_name = 'clinica/reportes/pacientes.html'

    def get_queryset(self):
        filtros = self.request.GET.get('filtros')
        todosLosPacientes()
        if filtros:
            q = Filtro.objects.get(id=filtros)
            fecha_actual = timezone.now().date()
            if q.filtro == 'Asistieron a los turnos en la semana/mes':
                query_reporte = q.filtro
                pacientes.clear()
                turnos = Turno.objects.filter(
                    Q(fecha__month=fecha_actual.month) and Q(asistencia='A')
                )
                for turno in turnos:
                    paciente = Paciente.objects.get(id=turno.paciente.id)
                    pacientes.append(paciente)
            elif q.filtro == 'No asistieron a los turnos en la semana/mes':
                query_reporte = q.filtro
                pacientes.clear()
                turnos = Turno.objects.filter(
                    Q(fecha__month=fecha_actual.month) and Q(asistencia='F')
                )
                for turno in turnos:
                    paciente = Paciente.objects.get(id=turno.paciente.id)
                    pacientes.append(paciente)
            elif q.filtro == 'Hicieron por lo menos un pedido en la semana/mes':
                query_reporte = q.filtro
                pacientes.clear()
                pedidos = Pedido.objects.filter(created_at__month=fecha_actual.month)
                for pedido in pedidos:
                    paciente = Paciente.objects.filter(id=pedido.paciente.id)
                    pacientes.append(paciente)
            elif q.filtro == 'Todos':
                query_reporte = 'Pacientes'
                return pacientes
        return pacientes
        

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['form'] = FiltroPacientes
        contexto['titulo'] = 'Pacientes'
        return contexto 

def descargarPDF(peticion):
    if peticion.method == 'GET':
        contexto = {
            'reporte': query_reporte,
            'pacientes': pacientes,
            'titulo':'Pacientes'
        }
        pdf = generar_reporte_pdf(ListaPacientes.template_name, contexto)
        return HttpResponse(pdf, content_type='application/pdf')
    return HttpResponseRedirect(reverse_lazy('reportes:pacientes'))