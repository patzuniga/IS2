from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.signals import request_finished
from django.db.models.signals import post_save
from django.dispatch import receiver
#rom apps.viaje.models import Viaje
# Create your models here.

class Usuario(AbstractUser):
	usuario = models.CharField(max_length=30, null = False)
	#viajes = models.ManyToManyField(Viaje, null= True, blank=True, on_delete=models.CASCADE)
	def __str__(self):
		return self.username

	def is_conductor(self):
		try:
			return self._conductor
		except conductor.DoesNotExist:
			return 1
 
class Perfil(models.Model):
	usuario = models.OneToOneField(Usuario, on_delete = models.CASCADE, null = True, blank=True)
	rut = models.CharField(max_length=10, null = True, blank = True)
	nombre = models.CharField(max_length=30, null = True, blank = True)
	numero_teléfono = models.CharField(max_length=30, null = True, blank = True)
	dirección = models.CharField(max_length=40,null = True, blank = True)
	valoración = models.FloatField(null = True, blank = True)
	profesión = models.CharField(max_length=20, null = True, blank = True)
	fumador = models.NullBooleanField( blank = True)
	class Meta:
		verbose_name = "Perfil"
		verbose_name_plural = "Perfiles"
	def __str__(self):
		return self.usuario.username
	def nombre(self):
		return self.Nombre
@receiver(post_save, sender = Usuario)
def create_user_profile(sender,instance,created,**kwargs):
	if created:
		Perfil.objects.create(usuario=instance)

@receiver(post_save,sender=Usuario)
def save_user_profile(sender,instance, **kwargs):
	instance.perfil.save()

class Interes_Personal(models.Model):
	  interes = models.CharField(max_length=20, null = False)


