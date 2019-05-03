from django.conf.urls import url, include

from apps.viaje.views import viaje_view
from apps.viaje.views import viaje_listo, Viajelist

urlpatterns = [
#url(r'^$',index,name='index'),
url(r'nuevo$', viaje_view, name='viaje_crear'),
url(r'listo$', viaje_listo, name='viaje_listo'),
url(r'viajes$', Viajelist, name='viaje_list'),
]