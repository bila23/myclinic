from django.shortcuts import render
from . import views
from django.conf.urls import url

urlpatterns = [
    url('horario/consulta/', views.home, name="horario_consulta"),
    url('horario/find/q/', views.find_consulta, name='horario_consulta_query'),
    url('horario/find/today/', views.show_today, name='horario_cons_today'),
    url('today/nueva/cita/', views.nueva_cita_today, name='today_nueva_cita'),
]
