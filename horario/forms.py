from django import forms

class HorConsultaForm(forms.Form):
    vdate = forms.CharField(max_length=10)
