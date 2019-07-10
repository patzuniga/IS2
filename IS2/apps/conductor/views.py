from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from apps.conductor.models import Conductor
from apps.usuario.models import Usuario, Perfil
from apps.viaje.models import Tramo, Reserva, Viaje
from apps.conductor.forms import Conductor_Form

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
		print("Ahora es ",auto_a)
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
					print("Reserva",re.pk,"pide",re.plazas_pedidas,"plazas")
					print("Viaje",viaje.pk,"tiene",viaje.plazas_disponibles,"plazas disponibles")
					if viaje.conductor != conductor:
						aceptarreserva = False # La reserva corresponde a otro conductor
						print("Reserva", re.pk, "no es mia")
						continue

					#Se supone que al pedir la reserva se verifica si hay asientos disponibles y se descuentan del total, así que esta parte estaría de más
					if aceptarreserva:
						for tr in tram:#revisar disponibilidad de cada tramo
							print("Tramo",tr.pk,"tiene",tr.asientos_disponibles,"asientos disponibles")
							if re.plazas_pedidas > tr.asientos_disponibles:
								aceptarreserva = False # No debe aceptarse por falta de asientos
								print("Reserva", re.pk, "no se acepta porque tramo",tr.pk,"no da")
								break
					
					if aceptarreserva:#Si todos los tramos tienen disponibilidad, se puede aceptar la reserva
						print("Aceptar reserva", re.pk)
						re.estado = "Aceptada"
						re.save()
						conductor.reservas_por_aprobar -=1
						conductor.save()
						for tr in tram:#se tiene que actualizar la disponibilidad de asientos de cada tramo?
							tr.asientos_disponibles -= re.plazas_pedidas
							tr.save()
					else:#Rechazar las que no se puede aceptar?
						print("Rechazar reserva", re.pk)
						re.estado = "Rechazada"
						re.save()
						conductor.reservas_por_aprobar -=1
						conductor.save()


						
	return HttpResponseRedirect('/conductor/configuracion/')

def registro_conductor(request):
	if request.method == 'POST':
		if(request.POST.get("conductor")):
			form = Conductor_Form()
			return render(request, 'conductor/conductor.html', {'form': form})
		form = Conductor_Form(request.POST, request.FILES)
		print("WUat")
		if form.is_valid():
			print("valido")
			print(form.cleaned_data['consumo'])
			if(request.POST.get("registrarme")):
				print("registrarme")
				u = Usuario()
				u.username = request.session['usuario']['username'] 
				u.usuario = request.session['usuario']['username']
				u.first_name = request.session['usuario']['firstname']
				u.last_name  = request.session['usuario']['lastname']
				u.email = request.session['usuario']['email']
				u.set_password(request.session['usuario']['password'])
				u.save()
				p = u.perfil
				p.nombre = u.first_name + u.last_name
				p.usuario = u
				p.rut = request.session['usuario']['rut']
				p.numero_telefono = request.session['usuario']['numero_telefono']
				p.direccion = request.session['usuario']['direccion']
				p.profesion = request.session['usuario']['profesion']
				p.fumador = request.session['usuario']['fumador']
				p.save()
				v = Vehiculo()
				v.patente = form.cleaned_data['patente']
				v.marca = form.cleaned_data['marca']
				v.modelo = form.cleaned_data['modelo']
				v.maleta = form.cleaned_data['maleta']
				v.color = form.cleaned_data['color']
				v.Numeroasientos = form.cleaned_data['asientos']
				v.consumo = form.cleaned_data['consumo']
				print(form.cleaned_data['consumo'])
				v.foto = form.cleaned_data['foto']
				v.save()
				c = Conductor()
				c.clasedelicencia = form.cleaned_data['clasedelicencia']
				c.fecha_obtencion = form.cleaned_data['fecha_obtencion']
				c.usuario = u
				c.car = v
				c.save()
				return render(request, 'usuario/registrado.html', {})
			else:
				return redirect('index')
		else:
			return render(request, 'conductor/conductor.html', {'form': form})
	else:
		form = Conductor_Form()
		return render(request, 'conductor/conductor.html', {'form': form})

@login_required()
def valoracionesPendientesConductor(request):
	current_user = request.user
	u = Usuario.objects.get(id=current_user.id)
	evaluador = u.conductor_set.all()[0]
	res = Reserva.objects.all()
#	print(evaluador.usuario)
	porValorar = []
	for v in Viaje.objects.all():
		if v.conductor == evaluador:
#			print(evaluador.usuario)
			for reserva in res:
				if reserva.tramos.all()[0].viaje == v.id and (reserva.estado == "Por Valorar" or reserva.estado == "Por Valorar Conductor"):
#					print(reserva.usuario)
					aux = []
#					print(reserva.id)
					print(reserva.estado)
					aux.append(reserva.usuario)
					aux.append(reserva.id)
					porValorar.append(aux)
	return render(request, 'conductor/valoracionesPendientesConductor.html',{'porValorar':porValorar})	

#	else:
#		return render(request, 'conductor/valoracionesPendientesConductor')

@login_required()
def vPC(request):
	current_user = request.user
	u = Usuario.objects.get(id=current_user.id)
	conductor = u.conductor_set.all()[0]
	valoracion = []
	print(conductor.usuario)
	if request.method == 'POST':
		post = Valoracion()
		post.pasajeroEvaluado =	request.POST.get('pasajeroEvaluado')
		post.nota = request.POST.get('nota')
		post.comentario = request.POST.get('comentario')
		post.comentarioAnonimo = request.POST.get('anon')
		resID = request.POST.get('resID')
		print(post.pasajeroEvaluado)
#		print(post.nota)
#		print(post.comentario)
		print(post.comentarioAnonimo)
		print(resID)
		aux = []
		if(post.comentarioAnonimo == "True"):
			aux.append("Anonimo")
			aux.append(post.nota)
			aux.append(post.pasajeroEvaluado)
			aux.append(post.comentario)
			valoracion.append(aux)
			print(valoracion)			
			res = Reserva.objects.get(id=resID)
			if( res.estado == "Por Valorar Conductor"):
				res.estado = "Terminada"
				print(res.estado)
				#Agregar res.save()
			if (res.estado == "Por Valorar"):
				res.estado = "Por Valorar Pasajero"
				print(res.estado)
				#Agregar res.save()
			return HttpResponseRedirect('/conductor/valoracionesPendientesConductor/',{'valoracion':valoracion})
		else:
			aux.append(conductor.usuario)
			aux.append(post.nota)
			aux.append(post.pasajeroEvaluado)
			aux.append(post.comentario)
			valoracion.append(aux)
			print(valoracion)
			res = Reserva.objects.get(id=resID)
			if( res.estado == "Por Valorar Conductor"):
				res.estado = "Terminada"
				print(res.estado)					
				#Agregar res.save()
			if (res.estado == "Por Valorar"):
				res.estado = "Por Valorar Pasajero"
				print(res.estado)
				#Agregar res.save()
			return HttpResponseRedirect('/conductor/valoracionesPendientesConductor/',{'valoracion':valoracion})				


