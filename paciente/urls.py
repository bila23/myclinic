from django.shortcuts import render
from . import views
from django.conf.urls import url

urlpatterns = [
    url('paciente/nuevo/', views.paciente_home, name="paciente_home"),
    url('paciente/find/key', views.find_paciente_by_key, name="paciente_find_by_key"),
]
