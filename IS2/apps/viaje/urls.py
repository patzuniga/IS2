from django.conf.urls import url, include

from apps.viaje.views import viaje_view

urlpatterns = [
#url(r'^$',index,name='index'),
url(r'nuevo$', viaje_view, name='viaje_crear'),
#url(r'listar$', Viajelist.as_view(), name='viaje_list'),
]