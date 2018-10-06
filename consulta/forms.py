from django import forms
from core.models import Consultas

class ExpedienteForm(forms.ModelForm):
    class Meta:
        model = Consultas
        fields = ('id', 'id_medico', 'problema', 'diagnostico', 'tratamiento', 'recomendacion', 'talla', 'peso', 'presion_art',)
