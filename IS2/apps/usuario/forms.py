from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import *

class CustomUserCreationForm(UserCreationForm):

	class Meta(UserCreationForm):
		model = Usuario
		fields = ('username', 'password', 'email', 'usuario')

class CustomUserChangeForm(UserChangeForm):

	class Meta:
		model = Usuario
		fields = ('username', 'password', 'email', 'usuario')

class Registrationform(forms.Form):
    username = forms.CharField(max_length=15, label="Usuario")
    firstname = forms.CharField(max_length=15,label="Nombre")
    lastname = forms.CharField(max_length=15,label="Apellido")
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, 
   label="Contraseña")
    password1 = forms.CharField(widget=forms.PasswordInput, 
   label="Confirmar Contraseña")
    rut = forms.IntegerField(label = "RUT", max_value= 999999999, min_value=11111111)
    numero_telefono = forms.CharField(max_length=30, label = "Teléfono")
    direccion = forms.CharField(max_length=40, label = "Dirección")
    profesion = forms.CharField(max_length=20, label = "Profesión")
    fumador = forms.BooleanField(required = False, label = "Fumador")
    def clean_username(self):
    	username = self.cleaned_data.get('username')
    	username_qs = Usuario.objects.filter(username=username)
    	if username_qs.exists():
    		raise forms.ValidationError("El nombre de usuario ya está en uso")
    	return username

    def clean_password1(self):
        password = self.cleaned_data.get('password')
        password1 = self.cleaned_data.get('password1')
        if password and password1 and password != password1:
            raise forms.ValidationError("Las contraseñas ingresadas no coinciden")
        return password1

class EditarPerfil(forms.Form):
    username = forms.CharField(max_length=15, label="Usuario",widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(required=True,widget=forms.EmailInput(attrs={'class':'form-control'}))
    numero_telefono = forms.CharField(max_length=30, label = "Teléfono",widget=forms.TextInput(attrs={'class':'form-control'}))
    direccion = forms.CharField(max_length=40, label = "Dirección",widget=forms.TextInput(attrs={'class':'form-control'}))
    profesion = forms.CharField(max_length=20, label = "Profesión",widget=forms.TextInput(attrs={'class':'form-control'}))
    fumador = forms.BooleanField(required = False, label = "Fumador",widget=forms.CheckboxInput(attrs={'class':'w3-check'}))

class EditarPerfilConduct(forms.Form):
    username = forms.CharField(max_length=15, label="Usuario",widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(required=True,widget=forms.EmailInput(attrs={'class':'form-control'}))
    numero_telefono = forms.CharField(max_length=30, label = "Teléfono",widget=forms.TextInput(attrs={'class':'form-control'}))
    direccion = forms.CharField(max_length=40, label = "Dirección",widget=forms.TextInput(attrs={'class':'form-control'}))
    profesion = forms.CharField(max_length=20, label = "Profesión",widget=forms.TextInput(attrs={'class':'form-control'}))
    fumador = forms.BooleanField(required = False, label = "Fumador",widget=forms.CheckboxInput(attrs={'class':'w3-check'}))
    maleta = forms.BooleanField( required = False, label = "Maleta",widget=forms.CheckboxInput(attrs={'class':'w3-check'}))
    clasedelicencia = forms.CharField(max_length=1, label = "Clase Licencia",widget=forms.TextInput(attrs={'class':'form-control'}))
    fecha_obtencion = forms.CharField(max_length=30,label = "Fecha obtencion Licencia",widget=forms.TextInput(attrs={'class':'form-control'}))
    patente = forms.CharField(max_length=30, label = "Patente Vehiculo",widget=forms.TextInput(attrs={'class':'form-control'}))
    marca = forms.CharField(max_length=30, label = "Marca Vehiculo",widget=forms.TextInput(attrs={'class':'form-control'}))
    modelo = forms.CharField(max_length=30, label = "Modelo Vehiculo",widget=forms.TextInput(attrs={'class':'form-control'}))
    color = forms.CharField(max_length=30, label = "Color Vehiculo",widget=forms.TextInput(attrs={'class':'form-control'}))
    Numeroasientos = forms.IntegerField( label = "Número de Asientos",widget=forms.NumberInput(attrs={'class':'form-control'}))
    consumo = forms.IntegerField( label = "Consumo Vehiculo(Kms/H)",widget=forms.NumberInput(attrs={'class':'form-control'}))
  
class Cambiarcontraseña(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput,label="Contraseña")
    password1 = forms.CharField(widget=forms.PasswordInput,label="Confirmar Contraseña")
    def clean_password1(self):
        password = self.cleaned_data.get('password')
        password1 = self.cleaned_data.get('password1')
        if password and password1 and password != password1:
            raise forms.ValidationError("Las contraseñas ingresadas no coinciden")
        return password1  
