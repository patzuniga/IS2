from django.contrib import admin
from apps.viaje.models import Viaje
from .models import Vehiculo
from .models import Conductor
# Register your models here.

class cond(admin.ModelAdmin):
	class Meta:
		model = Conductor
	list_display = ['id','usuario', 'clasedelicencia', 'car']

class vec(admin.ModelAdmin):
	class Meta:
		model = Vehiculo
	list_display = ['id', 'patente', ]

admin.site.register(Vehiculo, vec)
admin.site.register(Conductor, cond)
