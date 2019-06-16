from django.db import models
from apps.conductor.models import Conductor
from apps.usuario.models import Usuario
#from apps.usuario.models import *

# Create your models here.
class Parada(models.Model):
	nombre = models.CharField(max_length=40,null=False, default = "Concepcion")
	direccion = models.CharField(max_length=40,null=False)

	class Meta:
		verbose_name = "Parada"
		verbose_name_plural = "Paradas"

	def __unicode__(self):
		return self.nombre

class Tramo(models.Model):
	orden_en_viaje  = models.IntegerField(null=True,blank=True)
	hora_salida = models.TimeField(null=False, default = "15:00")
	hora_llegada = models.TimeField(null=False, default = "15:00")
	fecha = models.DateField()
	asientos_disponibles =  models.IntegerField(null=True,blank=True)
	origen = models.ForeignKey(Parada,related_name="ParadaOrigen", null=True, blank=True, on_delete = models.CASCADE,)
	destino = models.ForeignKey(Parada,related_name="ParadaDestino", null=True, blank=True, on_delete = models.CASCADE,)
	distancia  = models.FloatField(null=True,blank=True)
	viaje = models.IntegerField(null=True,blank=True)
	class Meta:
		verbose_name = "Tramo"
		verbose_name_plural = "Tramos"

	def __unicode__(self):
		return str(self.id)
class Viaje(models.Model):
	fecha = models.DateField()
	estado = models.CharField(max_length=20,null=False)
	porta_maleta = models.BooleanField(default=False)
	silla_niños = models.BooleanField(default=False)
	mascotas =  models.BooleanField(default=False)
	tarifaPreferencias = models.IntegerField(null=True,blank=True)
	plazas_disponibles = models.IntegerField(null=True,blank=True)
	tramos = models.ManyToManyField(Tramo, null = False, related_name = "Tramos")
	conductor = models.ForeignKey(Conductor, null= True, blank=True, on_delete = models.CASCADE,)

	class Meta:
		verbose_name = "Viaje"
		verbose_name_plural = "Viajes"

	def __unicode__(self):
		return str(self)

	def _tramos(self):
		return self.tramos

class Reserva(models.Model):
	estado = models.CharField(max_length=11)
	precio = models.IntegerField()
	plazas_pedidas = models.IntegerField()
	usuario = models.ForeignKey(Usuario, null= True, blank=True, on_delete = models.CASCADE)
	tramos = models.ManyToManyField(Tramo, null = False, related_name="reservas")