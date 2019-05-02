from django.db import models
#rom apps.viaje.models import Viaje
# Create your models here.

class Usuario(models.Model):
	nombre = models.CharField(max_length=50)
	apellidos = models.CharField(max_length=70)
	edad = models.IntegerField()
	email = models.EmailField()
	domicilio = models.TextField()
	rut = models.IntegerField()
	#viajes = models.ManyToManyField(Viaje, null= True, blank=True, on_delete=models.CASCADE)