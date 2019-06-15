from django.conf.urls import url, include
from apps.conductor.views import *

urlpatterns = [
    url(r'^configuracion/', configuracion, name='configuracion'),
#	url(r'^configuracion/cambio/', cambio, name='cambio'),
]
