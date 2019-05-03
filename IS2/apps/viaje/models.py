from django.db import models

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
	hora_salida = models.CharField(max_length=30,null=False, default = "15:00")
	hora_llegada = models.CharField(max_length=30,null=False, default = "15:00")
	fecha = models.CharField(max_length=30,null=False, default = "21/10/18")
	asientos_disponibles =  models.IntegerField(null=True,blank=True)
	origen = models.ForeignKey("Parada",related_name="ParadaOrigen", null=True, blank=True)
	destino = models.ForeignKey("Parada",related_name="ParadaDestino", null=True, blank=True)
	
	class Meta:
		verbose_name = "Tramo"
		verbose_name_plural = "Tramos"

	def __unicode__(self):
		return str(self.id_trayecto)

class Viaje(models.Model):
	Fecha = models.DateTimeField()
	Estado = models.CharField(max_length=20,null=False)
	Porta_maleta = models.BooleanField(default=False)
	Silla_niños = models.BooleanField(default=False)
	Mascotas =  models.BooleanField(default=False)
	TarifaPreferencias = models.IntegerField(null=True,blank=True)
	Max_personas_atras = models.IntegerField(null=True,blank=True)
	tramos = models.ManyToManyField(Tramo, null = False)

	class Meta:
		verbose_name = "Viaje"
		verbose_name_plural = "Viajes"

	def __unicode__(self):
		return str(self.id_viaje)




	