from django.conf.urls import url, include
from apps.conductor.views import *

urlpatterns = [
    url(r'^configuracion/', configuracion, name='configuracion'),
	url(r'^cambio/', cambio, name='cambio'),
	url(r'^registro$',registro_conductor, name= 'registro_conductor'),
]
