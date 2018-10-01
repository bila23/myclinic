from django.shortcuts import render
from . import views
from django.conf.urls import url

urlpatterns = [
    url('expediente/paciente/', views.home, name="expediente_paciente"),
    url('expediente/edit/(?P<pk>\d+)/$', views.update, name="expediente_update"),
]
