from django.contrib import admin
from .models import Viaje
from .models import Usuario
from .models import Vehiculo
from .models import Conductor
# Register your models here.

admin.site.register(Usuario)
admin.site.register(Viaje)
admin.site.register(Vehiculo)
admin.site.register(Conductor)
