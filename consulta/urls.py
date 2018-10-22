from django.shortcuts import render
from . import views
from django.conf.urls import url

urlpatterns = [
    url('expediente/paciente/', views.home, name="expediente_paciente"),
    url('expediente/edit/(?P<pk>\d+)/$', views.update, name="expediente_update"),
    url('expediente/ref/(?P<pk>\d+)/$', views.find_ref, name="find_ref"),
    url('expediente/save/ref/', views.save_ref, name="save_ref"),
    url('expediente/delete/ref/', views.delete_ref, name="delete_ref"),
    url('expediente/read/ref/', views.get_by_key, name="get_by_key_ref"),
    url('expediente/update/ref/', views.update_ref, name="update_ref"),
    url('expediente/med/(?P<pk>\d+)/$', views.find_med, name="find_med"),
    url('expediente/med/save/', views.save_med, name="save_med"),
    url('expediente/med/delete/', views.delete_med, name="delete_med"),
    url('expediente/med/get_by_key/', views.get_by_key_med, name="get_by_key_med"),
    url('expediente/med/update/', views.update_med, name="update_med"),
    url('expediente/exa/(?P<pk>\d+)/$', views.find_exa, name="find_exa"),
    url('expediente/exa/save/', views.save_exa, name="save_exa"),
    url('expediente/exa/delete/', views.delete_exa, name="delete_exa"),
    url('expediente/exa/get_by_key/', views.get_by_key_exa, name="get_by_key_exa"),
    url('expediente/exa/update/', views.update_exa, name="update_exa"),
]
