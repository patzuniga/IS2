from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from apps.usuario.models import Usuario
from apps.viaje.models import Reserva,Viaje

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

def confirmacion(request, pk):
	return render(request, 'usuario/confirmacion.html',{'id':pk})

def cancelar_reserva(request, pk):
	reserva = Reserva.objects.filter(id=pk)
	try:
		tramitos = reserva.tramos.all()
		now = datetime.now()
		if(tramitos[0].fecha ==  now.date()):
			if(tramitos[0].hora_salida > now.time + datetime.timedelta(hours = 2)):
				reserva[0].delete()
				success = True
			else:
				success = False
		elif(tramitos[0].fecha < now.date()):
			reserva[0].delete()
			success = True
		else:
			success = False
	except:
		success = False
	return render(request, 'usuario/cancelar_reserva.html', {'exito': success})
