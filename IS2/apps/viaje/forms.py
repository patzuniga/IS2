from django import forms
from apps.viaje.models import Viaje
"""
class ViajeForm(forms.ModelForm):

	class Meta:
		model = Viaje


		fields = [
			'origen',
			'destino',
			'fecha',
		]
		labels = {
			'origen': 'Origen',
			'destino': 'Destino',
			'fecha':'Fecha',
		}
		widgets = {
			'origen': forms.TextInput(attrs={'class':'form-control'}),
			'destino': forms.TextInput(attrs={'class':'form-control'}),
			'fecha_rescate': forms.TextInput(attrs={'class':'form-control'}),
		}
"""