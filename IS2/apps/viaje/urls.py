from django.conf.urls import url, include
from apps.viaje.views import *

urlpatterns = [
 	url(r'^$',index,name='index'),
	url(r'^nuevo$', viaje_view, name='viaje_crear'),
	url(r'^success$', success, name='success'),
	url(r'^viajes$', Viajelist, name='viaje_list'),
	url(r'^paradas$', viaje_paradas, name='paradas'),
	url(r'^mapa$', viaje_ver, name='mapa_ejemplo'),
	url(r'^cancel$', cancelar_crear_viaje, name='cancelar_crear_viaje'),
	url(r'^buscarviaje', buscar_viaje, name='buscar_viaje'),
	url(r'^viajes/details/(?P<pk>\d+)/$',viaje_details, name='viaje_details'),
	url(r'^editarviaje/(?P<idviaje>\d+)/$', editarviaje, name='editarviaje'),
	url(r'^confirmarCan/(?P<pk>\d+)/$', confirmarCan, name='confirmarCan'),
	url(r'^cancelar/(?P<pk>\d+)/$', cancelar, name='cancelar'),
	url(r'^realizar_reservas$', realizar_reservas, name='realizar_reservas'),
	url(r'^guardar_reservas$', guardar_reservas, name='guardar_reservas'),
	url(r'^error1$', error1 , name='cancelar_editar_error'),
	url(r'^confirmarCanReservaConductor/(?P<pk>\d+)/$', confirmarCanReservaConductor, name='confirmarCanReservaConductor'),
	url(r'^confirmarCanReservaAceptadaConductor/(?P<pk>\d+)/$', confirmarCanReservaAceptadaConductor, name='confirmarCanReservaAceptadaConductor'),
    url(r'^cancelarReservaAceptadaConductor/(?P<pk>\d+)/$', cancelarReservaAceptadaConductor, name='cancelarReservaAceptadaConductor'),
    url(r'^cancelarReservaConductor/(?P<pk>\d+)/$', cancelarReservaConductor, name='cancelarReservaConductor'),
    url(r'^confirmarAceptarReservaConductor/(?P<pk>\d+)/$', confirmarAceptarReservaConductor, name='confirmarAceptarReservaConductor'),
    url(r'^aceptarReservaConductor/(?P<pk>\d+)/$', aceptarReservaConductor, name='aceptarReservaConductor'),
]