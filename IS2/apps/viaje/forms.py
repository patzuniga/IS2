from django import forms
from apps.viaje.models import Viaje
from datetime import datetime
import pytz

from .models import *

class ViajeForm(forms.Form):

	fecha = forms.DateField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Fecha Destino (DD/MM/YY)'}))
	hora_origen = forms.TimeField(widget=forms.TimeInput(attrs={'class':'form-control','placeholder':'Hora Origen (HH:MM)'}))
	porta_maleta = forms.BooleanField(required = False,widget=forms.CheckboxInput(attrs={'class':'w3-check'}))
	silla_niños = forms.BooleanField(required = False,widget=forms.CheckboxInput(attrs={'class':'w3-check'}))
	mascotas = forms.BooleanField(required = False,widget=forms.CheckboxInput(attrs={'class':'w3-check'}))
	tarifapreferencias = forms.IntegerField(min_value=1,widget=forms.NumberInput(attrs={'class':'form-control','placeholder':'Tarifa Preferencias, costo por kilometro recorrido'}))
	plazas_disponibles = forms.IntegerField(min_value=0,widget=forms.NumberInput(attrs={'class':'form-control','placeholder':'Plazas Disponibles'}))
	#origen = forms.CharField(label="origen")
	#destino = forms.CharField(label="destino")
	fecha_destino = forms.DateField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Fecha Destino (DD/MM/YY)'}))
	hora_destino = forms.TimeField(widget=forms.TimeInput(attrs={'class':'form-control','placeholder':'Hora Origen (HH:MM)'}))
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
	origen = forms.CharField(label="Origen",widget=forms.TextInput(attrs={'class':'form-control'}))
	destino = forms.CharField(label="Destino",widget=forms.TextInput(attrs={'class':'form-control'}))
	fecha = forms.DateField(label = "Fecha de inicio (DD/MM/YY)")
	hora_origen = forms.TimeField(label = "Hora Origen")
	porta_maleta = forms.BooleanField(required = False)
	silla_niños = forms.BooleanField(required = False)
	mascotas = forms.BooleanField(required = False)
	tarifapreferencias = forms.IntegerField(label = "Tarifa")
	asientos_disponibles = forms.IntegerField(label = "Asientos disponibles")
	fecha_destino = forms.DateField(label = "Fecha de Termino (DD/MM/YY)")
	hora_destino = forms.TimeField(label = "Hora Destino")

class ParadasForm(forms.Form):
	fecha = forms.DateField(label = "Fecha de llegada",widget=forms.TextInput(attrs={'class':'form-control'}))
	hora = forms.TimeField(label = "Fecha de llegada",widget=forms.TextInput(attrs={'class':'form-control'}))

class BuscarForm(forms.Form):
	#origen = forms.CharField(label = "Origen")
	#destino = forms.CharField(label = "Destino")
	fecha = forms.DateField(label = "Fecha",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'DD/MM/YY'}))
	def clean(self):
		cleaned_data = super().clean()
		f1 = datetime.strptime(cleaned_data.get("fecha").strftime("%d/%m/%Y") , "%d/%m/%Y")
		tz = pytz.timezone('Chile/Continental')
		actual = datetime.strptime(datetime.now(tz=tz).strftime("%d/%m/%Y") , "%d/%m/%Y")
		if(actual > f1):
			raise forms.ValidationError("La fecha indicada no pueden ser menor a la actual")