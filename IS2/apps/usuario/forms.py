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
    username = forms.CharField(max_length=15, label="Usuario")
    email = forms.EmailField(required=True)
    numero_telefono = forms.CharField(max_length=30, label = "Teléfono")
    direccion = forms.CharField(max_length=40, label = "Dirección")
    profesion = forms.CharField(max_length=20, label = "Profesión")
    fumador = forms.BooleanField(required = False, label = "Fumador")

  
class Cambiarcontraseña(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput,label="Contraseña")
    password1 = forms.CharField(widget=forms.PasswordInput,label="Confirmar Contraseña")
    def clean_password1(self):
        password = self.cleaned_data.get('password')
        password1 = self.cleaned_data.get('password1')
        if password and password1 and password != password1:
            raise forms.ValidationError("Las contraseñas ingresadas no coinciden")
        return password1  
