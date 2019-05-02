from django.db import models
from django.contrib.auth.models import AbstractUser
#rom apps.viaje.models import Viaje
# Create your models here.

class Usuario(AbstractUser):
	usuario = models.CharField(max_length=30, null = False)
	#viajes = models.ManyToManyField(Viaje, null= True, blank=True, on_delete=models.CASCADE)
	def __str__(self):
		return self.username