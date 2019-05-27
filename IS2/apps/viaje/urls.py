from django.conf.urls import url, include

from apps.viaje.views import viaje_view, success, viaje_paradas,viaje_ver
from apps.viaje.views import viaje_listo, Viajelist, buscar_viaje,viaje_details,editarviaje

urlpatterns = [
#url(r'^$',index,name='index'),
	url(r'^nuevo$', viaje_view, name='viaje_crear'),
	url(r'^success$', success, name='success'),
	url(r'^viajes$', Viajelist, name='viaje_list'),
	url(r'^paradas$', viaje_paradas, name='paradas'),
	url(r'^mapa_ejemplo$', viaje_ver, name='mapa_ejemplo'),
	url(r'^buscarviaje', buscar_viaje, name='buscar_viaje'),
	url(r'^viajes/details/(?P<pk>\d+)/$',viaje_details, name='viaje_details'),
	url(r'^editarviaje$', editarviaje, name='editarviaje'),
]