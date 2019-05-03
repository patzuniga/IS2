from django.contrib import admin
from apps.viaje.models import Viaje
from .models import Usuario
from .models import Vehiculo
from .models import Conductor
# Register your models here.
class CustomViaje(admin.ModelAdmin):
	class Meta:
		model = Viaje
	list_display = ['id', 'fecha', ]

class cond(admin.ModelAdmin):
	class Meta:
		model = Conductor
	list_display = ['id', 'clasedelicencia', ]

class vec(admin.ModelAdmin):
	class Meta:
		model = Vehiculo
	list_display = ['id', 'patente', ]



admin.site.register(Usuario)
admin.site.register(Viaje, CustomViaje)
admin.site.register(Vehiculo, vec)
admin.site.register(Conductor, cond)
