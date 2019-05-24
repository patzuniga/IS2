from django.contrib import admin
from .models import Viaje, Tramo, Parada
class CustomParada(admin.ModelAdmin):
	class Meta:
		model = Parada
	list_display = ['id', 'nombre', ]
class CustomTramo(admin.ModelAdmin):
	class Meta:
		model = Tramo
	list_display = ['id', 'origen', 'destino',]
class CustomViaje(admin.ModelAdmin):
	class Meta:
		model = Viaje
	list_display = ['id', 'conductor']



#admin.site.unregister(Viaje)
admin.site.register(Viaje, CustomViaje)
admin.site.register(Tramo, CustomTramo)
admin.site.register(Parada, CustomParada)


