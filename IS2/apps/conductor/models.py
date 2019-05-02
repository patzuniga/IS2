from django.db import models
from apps.usuario.models import Usuario 
from apps.viaje.models import Viaje
# Create your models here.


class Conductor(models.Model):
	licencia = models.IntegerField()
	clasedelicencia = models.CharField(max_length=1)
	fecha_obtencion = models.CharField(max_length=30,null=False)
	marca = models.CharField(max_length=30,null=False)
	modelo = models.CharField(max_length=30,null=False)
	user = models.OneToOneField(Usuario, null= True, blank=True, on_delete=models.CASCADE)
	viaje = models.ForeignKey(Viaje, null= True, blank=True, on_delete=models.CASCADE)
	