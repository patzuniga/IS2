from django.conf.urls import url, include

from apps.viaje.views import viaje_view, success, viaje_paradas,viaje_ver
from apps.viaje.views import viaje_listo, Viajelist, buscar_viaje

urlpatterns = [
#url(r'^$',index,name='index'),
	url(r'^nuevo$', viaje_view, name='viaje_crear'),
	url(r'^success$', success, name='success'),
	url(r'^viajes$', Viajelist, name='viaje_list'),
	url(r'^paradas$', viaje_paradas, name='paradas'),
	url(r'^mapa_ejemplo$', viaje_ver, name='mapa_ejempl'),
	url(r'^buscarviaje', buscar_viaje, name='buscar_viaje'),
]