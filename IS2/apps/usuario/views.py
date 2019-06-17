from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from apps.usuario.models import Usuario, Perfil
from apps.viaje.models import Reserva,Viaje
from apps.usuario.forms import Registrationform
from apps.conductor.views import registro_conductor
from datetime import datetime 
from datetime import timedelta
import pytz

@login_required()
def home(request):
	if request.user.is_authenticated is not None:
		try:
			current_user = request.user
			u = Usuario.objects.get(id=current_user.id)
			u.conductor_set.all()[0]
			return render(request, 'usuario/index2.html',{'user': u})
		except:
			return render(request, 'usuario/index.html',{})

@login_required()
def ver_reservas(request):
	r = Reserva.objects.filter(usuario=request.user)
	reservas =[]
	for reserva in r:
		tramos = reserva.tramos.all()
		aux = []
		aux.append(tramos[0].viaje)
		aux.append(Viaje.objects.get(id=tramos[0].viaje).conductor.usuario)
		aux.append(reserva.plazas_pedidas)
		aux.append(tramos[0].origen.nombre)
		aux.append(tramos[len(tramos)-1].destino.nombre)
		aux.append(tramos[0].fecha)
		aux.append(tramos[0].hora_salida)
		aux.append(tramos[len(tramos)-1].fecha)
		aux.append(tramos[len(tramos)-1].hora_llegada)
		aux.append(reserva.precio)
		aux.append(reserva.estado)
		aux.append(reserva.id)
		reservas.append(aux)
	return render(request, 'usuario/reservas.html',{'reservas' : reservas})

@login_required()
def confirmacion(request, pk):
	return render(request, 'usuario/confirmacion.html',{'id':pk})

@login_required()
def cancelar_reserva(request, pk):
	reservas = Reserva.objects.filter(id=pk)
	reserva = reservas[0] 
	try:
		tramitos = reserva.tramos.all()
		tz = pytz.timezone('Chile/Continental')
		actual = datetime.strptime(datetime.now(tz=tz).strftime("%d/%m/%Y %H:%M:%S") , "%d/%m/%Y %H:%M:%S")
		fecha_origen = datetime.strptime(datetime.combine(tramitos[0].fecha,tramitos[0].hora_salida).strftime("%d/%m/%Y %H:%M:%S") , "%d/%m/%Y %H:%M:%S")
		actual_2 = (actual + timedelta(hours=2))
		if(fecha_origen > actual_2):
			if(reserva.estado == "Por Aprobar"):
				v = Viaje.objects.get(id=tramitos[0].viaje)
				v.conductor.reservas_por_aprobar -= 1
				v.conductor.save()
			elif(reserva.estado == "Aprobada"):
				tramitos = reservas.tramos.all()
				for t in tramitos:
					t.asientos_disponibles -= reserva.plazas_pedidas
			reserva.delete()
			success = True
		else:
			success = False
	except:
		success = False
	return render(request, 'usuario/cancelar_reserva.html', {'exito': success})

def registro(request):
	if request.method == 'GET':
		form = Registrationform()
		return render(request, 'usuario/registrarme.html', {'form': form})
	elif request.method == 'POST':
		form = Registrationform(request.POST)
		if form.is_valid():
			if(request.POST.get("pasajero")):
				u = Usuario()
				u.username = form.cleaned_data['username']
				u.usuario = form.cleaned_data['username']
				u.first_name = form.cleaned_data['firstname']
				u.last_name  = form.cleaned_data['lastname']
				u.email = form.cleaned_data['email']
				u.set_password(form.cleaned_data['password'])
				u.save()
				p = u.perfil
				p.nombre = u.first_name + u.last_name
				p.usuario = u
				p.rut = form.cleaned_data['rut']
				p.numero_telefono = form.cleaned_data['numero_telefono']
				p.direccion = form.cleaned_data['direccion']
				p.profesion = form.cleaned_data['profesion']
				p.fumador = form.cleaned_data['fumador']
				p.save()
				return render(request, 'usuario/registrado.html', {})
			else:
				aux = dict()
				aux['username']= form.cleaned_data['username']
				aux['first_name'] = form.cleaned_data['firstname']
				aux['last_name']  = form.cleaned_data['lastname']
				aux['email'] = form.cleaned_data['email']
				aux['password'] = form.cleaned_data['password']
				aux['rut'] = form.cleaned_data['rut']
				aux['numero_telefono'] = form.cleaned_data['numero_telefono']
				aux['direccion'] = form.cleaned_data['direccion']
				aux['profesion'] = form.cleaned_data['profesion']
				aux['fumador'] = form.cleaned_data['fumador']
				request.session['usuario'] = aux
				return registro_conductor(request)
		else:
			return render(request, 'usuario/registrarme.html', {'form': form})
	else:
		form = Registrationform()
		return render(request, 'usuario/registrarme.html', {'form': form})