from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from apps.conductor.models import Conductor
from apps.usuario.models import Usuario, Perfil
from apps.viaje.models import Tramo, Reserva, Viaje

@login_required()
def configuracion(request):
	u = Usuario.objects.get(id=request.user.pk)
	conductor = u.conductor_set.all()[0]
	auto_a = conductor.autoaceptar_reservas
	print("Autoaceptar es",auto_a)
	return render(request, 'conductor/configuracion.html',{'auto_a':auto_a})

@login_required()
def cambio(request):
	u = Usuario.objects.get(id=request.user.pk)
	conductor = u.conductor_set.get(usuario=u) #all()[0]
	auto_a = conductor.autoaceptar_reservas
	print("Autoaceptar es",auto_a)
	if request.method == 'POST':
		auto_a = not auto_a
		print("Ahora es",auto_a)
		conductor.autoaceptar_reservas = auto_a
		conductor.save()

		if auto_a:#Aceptar reservas pendientes al activar
			reser = Reserva.objects.all()
			for re in reser:
				if re.estado == "Por Aprobar":
					tram = re.tramos.all()
					aceptarreserva = True
					#comprovar conductor del viaje
					viaje = Viaje.objects.get(pk=tram[0].viaje)
					#print("Reserva",re.pk,"pide",re.plazas_pedidas,"plazas")
					#print("Viaje",viaje.pk,"tiene",viaje.plazas_disponibles,"plazas disponibles")
					if viaje.conductor != conductor:
						aceptarreserva = False # La reserva corresponde a otro conductor
						print("Reserva", re.pk, "no es mia")

					#Se supone que al pedir la reserva se verifica si hay asientos disponibles y se descuentan del total, así que esta parte estaría de más
					#if aceptarreserva:
					#	for tr in tram:#revisar disponibilidad de cada tramo
					#		print("Tramo",tr.pk,"tiene",tr.asientos_disponibles,"asientos disponibles")
					#		if re.plazas_pedidas > tr.asientos_disponibles:
					#			aceptarreserva = False # No debe aceptarse por falta de asientos
					#			print("Reserva", re.pk, "no se acepta porque tramo",tr.pk,"no da")	
					
					if aceptarreserva:#Si todos los tramos tienen disponibilidad, se puede aceptar la reserva
						print("Aprobar reserva", re.pk)
						#re.estado = "Aprobada"
						#re.save()
						#for tr in tram:#se tiene que actualizar la disponibilidad de asientos de cada tramo?


						
	return HttpResponseRedirect('/conductor/configuracion/')