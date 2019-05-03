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

	fecha = forms.CharField(label = "Fecha de inicio (DD/MM/YY HH:MM)")
	estado = forms.CharField(required=False)
	porta_maleta = forms.BooleanField()
	silla_niños = forms.BooleanField()
	Mascotas = forms.BooleanField()
	tarifapreferencias = forms.IntegerField(label = "tarifa")
	max_personas_atras = forms.IntegerField(label = "Num personas atras")
	tramos = forms.CharField(label="tramos")