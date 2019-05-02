from django.conf.urls import url, include
from apps.usuario.views import index
urlpatterns = [
    url(r'^index', index),
]