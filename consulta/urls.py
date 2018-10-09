from django.shortcuts import render
from . import views
from django.conf.urls import url

urlpatterns = [
    url('expediente/paciente/', views.home, name="expediente_paciente"),
    url('expediente/edit/(?P<pk>\d+)/$', views.update, name="expediente_update"),
    url('expediente/ref/(?P<pk>\d+)/$', views.find_ref, name="find_ref"),
    url('expediente/save/ref/', views.save_ref, name="save_ref"),
    url('expediente/delete/ref/', views.delete_ref, name="delete_ref"),
]
