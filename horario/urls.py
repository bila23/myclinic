from django.shortcuts import render
from . import views
from django.conf.urls import url

urlpatterns = [
    url('horario/consulta/', views.home, name="horario_consulta"),
    url('horario/find/q/', views.find_consulta, name='horario_consulta_query'),
    url('horario/find/today/', views.show_today, name='horario_cons_today'),
    url('horario/save/pac/', views.save_pac_hor, name='horario_save_pac'),
    url('horario/del/pac/', views.delete_horario, name='horario_delete_pac'),
]
