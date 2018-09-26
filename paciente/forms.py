from django.forms import ModelForm
from core.models import Paciente
from django import forms

class PacienteForm(ModelForm):
    class Meta:
        model = Paciente
        fields = ['nombre', 'sexo', 'correo', 'celular', 'telefono_casa', 'telefono_oficina', 'aseguradora', 'dui', 'direccion', 'estado_civil', 'profesion', 'empresa', 'direccion_empresa', 'municipio']
        