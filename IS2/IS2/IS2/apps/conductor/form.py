from django import forms
from apps.conductor.modls import Conductor

class ConductorForm(forms.ModelForm):

	class Meta:
		model = Conductor

  		fields = [
          'nombre',
          'apellidos',
          'edad',


  		]
