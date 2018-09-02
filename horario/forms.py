from django import forms

class HorConsultaForm(forms.Form):
    date = forms.DateField()
