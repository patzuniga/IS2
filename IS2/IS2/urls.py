"""IS2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url, include
from django.conf.urls import include,url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from apps.usuario.views import my_view

urlpatterns = [
    #url(r'^login', auth_views.login, {'template_name': './login/login.html'}, name="login"),
    url(r'^logout',my_view),
    url(r'^$', my_view),
    url(r'^admin/', admin.site.urls),
    url(r'^conductor', include('apps.conductor.urls')),
    url(r'^usuario', include('apps.usuario.urls')),
    url(r'^viaje', include('apps.viaje.urls')),
]
