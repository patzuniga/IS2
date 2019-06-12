from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from .views import *
from django.contrib import admin
from django.conf.urls import url, include
from django.conf.urls import include,url
from django.contrib import admin

urlpatterns = [
	url(r'^login/$', auth_views.login, {'template_name': 'login/login.html'}, name='login'),
	url(r'logout$', auth_views.logout, {'next_page': '/'}, name="logout"),
	url(r'^$', home),
	url(r'^admin/', admin.site.urls),
	url(r'^viaje/', include('apps.viaje.urls')),
	url(r'^conductor/', include('apps.conductor.urls')),
]