from django.conf.urls import url, include
from apps.conductor.views import configuracion #index, 
urlpatterns = [
    #url(r'^$', index),
    url(r'^configuracion/', configuracion, name='configuracion'),
]
