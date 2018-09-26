from django.shortcuts import render
from . import views
from django.conf.urls import url

urlpatterns = [
    url('expediente/paciente', views.home, name="expediente_paciente"),
    url('expediente/save/paciente', views.save, name="expediente_save"),
]
