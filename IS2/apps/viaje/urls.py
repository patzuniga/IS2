from django.conf.urls import url, include

from apps.viaje.views import viaje_view, success, viaje_paradas
from apps.viaje.views import viaje_listo, Viajelist

urlpatterns = [
#url(r'^$',index,name='index'),
	url(r'^nuevo$', viaje_view, name='crear'),
	url(r'^success$', success, name='success'),
	url(r'^viajes$', Viajelist, name='viaje_list'),
	url(r'^paradas$', viaje_paradas, name='paradas'),
]