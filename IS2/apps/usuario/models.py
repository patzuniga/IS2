from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.signals import request_finished
from django.db.models.signals import post_save
from django.dispatch import receiver
#from apps.viaje.models import Tramo
# Create your models here.
 
class Usuario(AbstractUser):
	usuario = models.CharField(max_length=30, null = False)

class Perfil(models.Model):
	usuario = models.OneToOneField(Usuario, on_delete = models.CASCADE, null = True, blank=True, related_name = "perfil")
	rut = models.CharField(max_length=10, null = True, blank = True)
	nombre = models.CharField(max_length=30, null = True, blank = True)
	email = models.EmailField(max_length=70,blank=True)
	numero_telefono = models.CharField(max_length=30, null = True, blank = True)
	direccion = models.CharField(max_length=40,null = True, blank = True)
	valoracion = models.FloatField(default = 5.0)
	profesion = models.CharField(max_length=20, null = True, blank = True)
	fumador = models.NullBooleanField( blank = True)
	viajes_en_curso = models.IntegerField(default = 0)
	mensajes = models.CharField(max_length=50, default="")
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

class Valoracion(models.Model):
	nota = models.IntegerField(null= False, blank=False)
	usuarioEvaluador = models.ForeignKey(Usuario, null = True,on_delete = models.CASCADE, related_name="usuariosEvaluador")
	usuarioEvaluado = models.ForeignKey	(Usuario,  null = True,on_delete = models.CASCADE, related_name="usuariosEvaluado")
	comentario = models.TextField(null=False,blank=False)
	anonimo = models.BooleanField(default=False)
	class Meta:
		verbose_name = "Valoracion"
		verbose_name_plural = "Valoraciones"

