from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from apps.usuario.models import Usuario
from apps.viaje.models import Reserva,Viaje
from datetime import datetime 
from datetime import timedelta

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
		if(tramitos[0].fecha ==  datetime.now().strftime("%d/%m/%Y") ):
			if(tramitos[0].hora_salida.strftime('%H:%M:%S') > (datetime.now() + timedelta(hours=2)).strftime('%H:%M:%S')):
				for t in tramitos:
					t.asientos_disponibles += reserva.plazas_pedidas
					t.save()
				if(reserva.estado == "Por aprobar"):
					v = Viaje.objects.get(id=tramitos[0].viaje)
					v.conductor.reservas_por_aprobar -= 1
					v.conductor.save()
				reserva.delete()
				success = True
			else:
				success = False
		elif(tramitos[0].fecha < datetime.now().strftime("%d/%m/%Y")):
			for t in tramitos:
					t.asientos_disponibles += reserva.plazas_pedidas
					t.save()
			if(reserva.estado == "Por aprobar"):
					v = Viaje.objects.get(id=tramitos[0].viaje)
					v.conductor.reservas_por_aprobar -= 1
					v.conductor.save()
			reserva.delete()
			success = True
		else:
			success = False
	except:
		success = False
	return render(request, 'usuario/cancelar_reserva.html', {'exito': success})
