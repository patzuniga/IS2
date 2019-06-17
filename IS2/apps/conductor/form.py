from django import forms
from apps.conductor.models import Conductor

class ConductorForm(forms.ModelForm):

	class Meta:
		model = Conductor
		fields = ['clasedelicencia','fecha_obtencion',]
 
class Conductor_Form(forms.Form):
 	clasedelicencia = forms.CharField(max_length=1, label = "Clase Licencia")
 	fecha_obtencion = forms.CharField(max_length=30,label = "Fecha obtencion Licencia")
 	patente = forms.CharField(max_length=30, label = "Patente Vehiculo")
 	marca = forms.CharField(max_length=30, label = "Marca Vehiculo")
 	modelo = forms.CharField(max_length=30, label = "Modelo Vehiculo")
 	maleta = forms.BooleanField( required = False, label = "Maleta")
 	color = forms.CharField(max_length=30, label = "Color Vehiculo")
 	Numeroasientos = forms.IntegerField( label = "Número de Asientos")
 	consumo = forms.IntegerField( label = "Consumo Vehiculo")
 	foto = forms.ImageField( label = "Foto Vehiculo")
