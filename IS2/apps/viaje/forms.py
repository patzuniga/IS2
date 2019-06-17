from django import forms
from apps.viaje.models import Viaje
from datetime import datetime
import pytz
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

	fecha = forms.DateField(label = "Fecha (DD/MM/YY)")
	porta_maleta = forms.BooleanField(required = False)
	silla_niños = forms.BooleanField(required = False)
	mascotas = forms.BooleanField(required = False)
	tarifapreferencias = forms.IntegerField(label = "Tarifa" , min_value= 0)
	plazas_disponibles = forms.IntegerField(label = "Plazas disponibles", min_value= 0)
	#origen = forms.CharField(label="origen")
	hora_origen = forms.TimeField(label = "Hora Origen")
	#destino = forms.CharField(label="destino")
	fecha_destino = forms.DateField(label = "Fecha (DD/MM/YY)")
	hora_destino = forms.TimeField(label = "Hora Destino")
	
	def clean(self):
		cleaned_data = super().clean()
		f1 = cleaned_data.get("fecha")
		h1 = cleaned_data.get("hora_origen")
		f2 = cleaned_data.get("fecha_destino")
		h2 = cleaned_data.get("hora_destino")
		tz = pytz.timezone('Chile/Continental')
		actual = datetime.strptime(datetime.now(tz=tz).strftime("%d/%m/%Y %H:%M:%S") , "%d/%m/%Y %H:%M:%S")
		fecha_origen = datetime.strptime(datetime.combine(f1,h1).strftime("%d/%m/%Y %H:%M:%S") , "%d/%m/%Y %H:%M:%S")
		fecha_destino = datetime.strptime(datetime.combine(f2,h2).strftime("%d/%m/%Y %H:%M:%S") , "%d/%m/%Y %H:%M:%S")
		if(actual > fecha_origen or actual > fecha_destino):
			raise forms.ValidationError("Las fechas indicadas no pueden ser menores a la actual")
		elif (fecha_destino <= fecha_origen):
			raise forms.ValidationError("Fecha y hora de término deben ser mayores a la fecha y hora de inicio.")

class EditarViajeForm(forms.Form):
	fecha = forms.DateField(label = "Fecha de inicio (DD/MM/YY)")
	porta_maleta = forms.BooleanField(required = False)
	silla_niños = forms.BooleanField(required = False)
	mascotas = forms.BooleanField(required = False)
	tarifapreferencias = forms.IntegerField(label = "Tarifa")
	max_personas_atras = forms.IntegerField(label = "Num personas atras")
	#origen = forms.CharField(label="origen")
	hora_origen = forms.TimeField(label = "Hora Origen")
	#destino = forms.CharField(label="destino")
	fecha_destino = forms.DateField(label = "Fecha de Termino (DD/MM/YY)")
	hora_destino = forms.TimeField(label = "Hora Destino")

	def clean(self):
		cleaned_data = super().clean()
		f1 = cleaned_data.get("fecha")
		h1 = cleaned_data.get("hora_origen")
		f2 = cleaned_data.get("fecha_destino")
		h2 = cleaned_data.get("hora_destino")
		tz = pytz.timezone('Chile/Continental')
		actual = datetime.strptime(datetime.now(tz=tz).strftime("%d/%m/%Y %H:%M:%S") , "%d/%m/%Y %H:%M:%S")
		fecha_origen = datetime.strptime(datetime.combine(f1,h1).strftime("%d/%m/%Y %H:%M:%S") , "%d/%m/%Y %H:%M:%S")
		fecha_destino = datetime.strptime(datetime.combine(f2,h2).strftime("%d/%m/%Y %H:%M:%S") , "%d/%m/%Y %H:%M:%S")
		if(actual > fecha_origen or actual > fecha_destino):
			raise forms.ValidationError("Las fechas indicadas no pueden ser menores a la actual")
		if (fecha_destino <= fecha_origen):
			raise forms.ValidationError("Fecha y hora de termino deben ser mayores a la fecha y hora de inicio.")

class ParadasForm(forms.Form):
	fecha = forms.DateField(label = "Fecha de llegada")
	hora = forms.TimeField(label = "Hora de llegada")

class BuscarForm(forms.Form):
	#origen = forms.CharField(label = "Origen")
	#destino = forms.CharField(label = "Destino")
	fecha = forms.DateField(label = "Fecha (DD/MM/YY)")
	def clean(self):
		cleaned_data = super().clean()
		f1 = datetime.strptime(cleaned_data.get("fecha").strftime("%d/%m/%Y") , "%d/%m/%Y")
		tz = pytz.timezone('Chile/Continental')
		actual = datetime.strptime(datetime.now(tz=tz).strftime("%d/%m/%Y") , "%d/%m/%Y")
		if(actual > f1):
			raise forms.ValidationError("La fecha indicada no pueden ser menor a la actual")
