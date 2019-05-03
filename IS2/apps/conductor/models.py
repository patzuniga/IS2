from django.db import models
from apps.usuario.models import Usuario 
from apps.viaje.models import Viaje
# Create your models here.

class Vehiculo(models.Model):
	pantete = models.CharField(max_length=30,null=False)
	marca = models.CharField(max_length=30,null=False)
	modelo = models.CharField(max_length=30,null=False)
	maleta = models.BooleanField(default=False)

class Conductor(models.Model):
	licencia = models.IntegerField()
	clasedelicencia = models.CharField(max_length=1)
	fecha_obtencion = models.CharField(max_length=30,null=False)
	user = models.OneToOneField(Usuario, null= True, blank=True, on_delete=models.CASCADE)
	viaje = models.ForeignKey(Viaje, null= True, blank=True, on_delete=models.CASCADE)
	car = models.OneToOneField(Vehiculo, null = True, blank = True, on_delete=models.CASCADE)
	
	class Meta:
		verbose_name = "Conductor"
		verbose_name_plural = "Conductores"

	def __unicode__(self):
		return str(self.id)

