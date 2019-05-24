from django import forms
from apps.viaje.models import Viaje
"""
class ViajeForm(forms.Form):

	class Meta:
		model = Viaje


		fields = [
			'fecha',
			'estado',
			'porta_maleta',
			'silla_niños',
			'mascotas',
			'tarifapreferencias',
			'max_personas_atras',
			'tramos',
		]
		labels = {
			'fecha': 'Fecha',
			'estado': 'Estado',
			'porta_maleta': 'Porta_maleta',
			'silla_niños': 'Silla_niños',
			'mascotas':'Mascotas',
			'tarifapreferencias' : 'Tarifapreferencias',
			'max_personas_atras': 'Max_personas_atras',
			'tramos' : 'Tramos',
		}
		widgets = {
			'fecha' : forms.DateInput(attrs={'class':'form-control'}),
			'estado' : forms.TextInput(attrs={'class':'form-control'}),
			'porta_maleta' : forms.NullBooleanSelect(attrs={'class':'form-control'}),
			'silla_niños' : forms.NullBooleanSelect(attrs={'class':'form-control'}),
			'mascotas' : forms.NullBooleanSelect(attrs={'class':'form-control'}),
			'tarifapreferencias' : forms.NumberInput(attrs={'class':'form-control'}),
			'max_personas_atras' : forms.NumberInput(attrs={'class':'form-control'}),
			'tramos' : forms.TextInput(attrs={'class':'form-control'}),
		}
"""
from .models import *

class ViajeForm(forms.Form):

	fecha = forms.DateField(label = "Fecha de inicio")
	porta_maleta = forms.BooleanField(required = False)
	silla_niños = forms.BooleanField(required = False)
	mascotas = forms.BooleanField(required = False)
	tarifapreferencias = forms.IntegerField(label = "tarifa")
	max_personas_atras = forms.IntegerField(label = "Num personas atras")
	origen = forms.CharField(label="origen")
	hora_origen = forms.CharField(label = "Hora Origen")
	destino = forms.CharField(label="destino")
	fecha_destino = forms.DateField(label = "Fecha de Termino")
	hora_destino = forms.CharField(label = "Hora Destino")

class ParadasForm(forms.Form):
	fecha = forms.DateField(label = "Fecha de llegada")
	hora = forms.CharField(label = "Hora de llegada")