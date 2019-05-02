from django.conf.urls import url, include
from apps.conductor.views import index
urlpatterns = [
    url(r'^$', index),
]
