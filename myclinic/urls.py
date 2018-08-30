from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.contrib.auth import views
from django.views.generic.base import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^login/$', views.LoginView.as_view(), {'template_name': 'registration/login.html'}, name='login'),
    url(r'^logout/$', views.LogoutView.as_view(), {'next_page': '/login'}, name='logout'),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path(r'', include('core.urls')),
]
