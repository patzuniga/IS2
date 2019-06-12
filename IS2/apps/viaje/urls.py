from django.conf.urls import url, include
<<<<<<< HEAD

from apps.viaje.views import viaje_view, success, viaje_paradas,viaje_ver
from apps.viaje.views import viaje_listo, Viajelist, buscar_viaje,viaje_details,editarviaje,confirmarCan, realizar_reservas, cancelar
=======
from apps.viaje.views import *
>>>>>>> 5c35377cd99f48bf6e7efcc1fd362845204bff32

urlpatterns = [
 	url(r'^$',index,name='index'),
	url(r'^nuevo$', viaje_view, name='viaje_crear'),
	url(r'^success$', success, name='success'),
	url(r'^viajes$', Viajelist, name='viaje_list'),
	url(r'^paradas/(?P<pk>\d+)/$', viaje_paradas, name='paradas'),
	url(r'^mapa_ejemplo/(?P<pk>\d+)/$', viaje_ver, name='mapa_ejemplo'),
	url(r'^buscarviaje', buscar_viaje, name='buscar_viaje'),
	url(r'^viajes/details/(?P<pk>\d+)/$',viaje_details, name='viaje_details'),
	url(r'^editarviaje$', editarviaje, name='editarviaje'),
	url(r'^confirmarCan/(?P<pk>\d+)/$', confirmarCan, name='confirmarCan'),
	url(r'^cancelar/(?P<pk>\d+)/$', cancelar, name='cancelar'),
	url(r'^realizar_reservas/(?P<pk>\d+)/$', realizar_reservas, name='realizar_reservas'),
]