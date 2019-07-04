from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from .views import *
from django.contrib import admin
from django.conf.urls import url, include
from django.conf.urls import include,url
from django.contrib import admin

urlpatterns = [
	url(r'^login/$', auth_views.login, {'template_name': 'login/login.html'}, name='login'),
	url(r'^registro$',registro, name= 'registro'),    
	url(r'logout$', auth_views.logout, {'next_page': '/'}, name="logout"),
	url(r'^$', home, name='home'),
	url(r'^admin/', admin.site.urls),
	url(r'^viaje/', include('apps.viaje.urls')),
	url(r'^conductor/', include('apps.conductor.urls')),
	url(r'^ver_reservas/',ver_reservas, name= 'ver_reservas'),
	url(r'^cancelar/(?P<pk>\d+)/$',confirmacion, name = 'confirmacion'),
	url(r'^cancelar/done/(?P<pk>\d+)/$',cancelar_reserva, name= 'cancelar_reserva'),  
	url(r'^password/$', editarperfil, name='editarperfil'),   
	url(r'^perfil/',ver_perfil, name= 'ver_perfil'),
	]