from django.shortcuts import render
from . import views
from django.conf.urls import url

urlpatterns = [
    url('horario/consulta/', views.home, name="horario_consulta"),
]
