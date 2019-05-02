from django.db import models
from django.contrib.auth.models import AbstractUser
#rom apps.viaje.models import Viaje
# Create your models here.

class Usuario(AbstractUser):
	nombre = models.CharField(max_length=50)
	apellidos = models.CharField(max_length=70)
	edad = models.IntegerField()
	email = models.EmailField()
	domicilio = models.TextField()
	rut = models.IntegerField()
	profesion = models.CharField(max_length=30,null=False, default=" ")
	interes = models.CharField(max_length=30,null=False, default=" ")
	fumador = models.CharField(max_length=30,null=False, default=" ")	

	#viajes = models.ManyToManyField(Viaje, null= True, blank=True, on_delete=models.CASCADE)

