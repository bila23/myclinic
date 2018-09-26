from django import forms

class ExpedienteForm(forms.Form):
    id_int = forms.IntegerField(),
    id_horario = forms.IntegerField(),
    id_paciente = forms.IntegerField(),
    fecha = forms.DateField(),
    problema = forms.CharField(),
    diagnostico = forms.CharField(),
    tratamiento = forms.CharField(),
    recomendacion = forms.CharField(),
    talla = forms.DecimalField(),
    peso = forms.DecimalField(),
    pres_art = forms.DecimalField()
