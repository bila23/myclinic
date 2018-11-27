from django.shortcuts import render
from . import views
from django.conf.urls import url

urlpatterns = [
    url('paciente/nuevo/', views.paciente_home, name="paciente_home"),
    url('paciente/find/key', views.find_paciente_by_key, name="paciente_find_by_key"),
    url('paciente/save', views.save_paciente, name="paciente_save"),
    url('paciente/find/', views.find_pacientes, name="paciente_find"),
    url('paciente/all', views.find_pacientes_all, name="paciente_find_all"),
    url('paciente/get/single', views.get_paciente_by_key, name="get_paciente_by_key"),
]
