# Modelos
from django.contrib.auth.models import Group

def run():
    """ 
    Crea los grupos que necesita el sistema para funcionar. 
    > python manage.py runscript script_grupos
    """
    Group.objects.bulk_create([
        Group(name="Medico"),
        Group(name="Secretaria"),
        Group(name="Gerencia"),
        Group(name="Venta"),
        Group(name="Taller")
    ])