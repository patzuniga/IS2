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
			return render(request, 'usuario/index2.html',{})
		except:
			return render(request, 'usuario/index.html',{})

def ver_reservas(request):
	r = Reserva.objects.filter(usuario=request.user)
	print(r)
	aux = []
	for reserva in r:
		tramos = reserva.tramos.all()
		aux.append(tramos[0].viaje)
		aux.append(Viaje.objects.get(id=tramos[0].viaje))
		aux.append(reserva.plazas_pedidas)
		aux.append(tramos[0].origen.nombre)
		aux.append(tramos[len(tramos)-1].destino.nombre)
		aux.append(tramos[0].fecha)
		aux.append(tramos[0].hora_salida)
		aux.append(tramos[len(tramos)-1].fecha)
		aux.append(tramos[len(tramos)-1].hora_llegada)
		aux.append(reserva.precio)
		aux.append(reserva.estado)
		print(reserva.id)
	return render(request, 'usuario/reservas.html',{'reservas' : aux})