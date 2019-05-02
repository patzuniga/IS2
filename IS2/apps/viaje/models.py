from django.db import models

# Create your models here.


class Viaje(models.Model):
	origen = models.CharField(max_length=40)
	destino = models.CharField(max_length=40)
	fecha = models.DateTimeField()
	