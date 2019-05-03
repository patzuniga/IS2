from django.contrib import admin
from .models import Viaje, Tramo, Parada


admin.site.unregister(Viaje)
admin.site.register(Viaje)
admin.site.register(Tramo)
admin.site.register(Parada)


