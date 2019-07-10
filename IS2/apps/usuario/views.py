from __future__ import unicode_literals
 
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from apps.usuario.models import Usuario, Perfil, Valoracion
from apps.conductor.models import Vehiculo, Conductor
from apps.viaje.models import Reserva,Viaje
from apps.usuario.forms import *
from apps.conductor.views import registro_conductor
from apps.conductor.views import Conductor, registro_conductor
from django.http import HttpResponseRedirect, HttpResponse
from datetime import datetime 
from datetime import timedelta
import pytz

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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
		aux.append(Viaje.objects.get(id=tramos[0].viaje).estado)
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
		print(actual_2 < fecha_origen)
		if(fecha_origen > actual_2):
			print("wuat")
			if(reserva.estado == "Por Aprobar"):
				v = Viaje.objects.get(id=tramitos[0].viaje)
				v.conductor.reservas_por_aprobar -= 1
				v.conductor.save()
			elif(reserva.estado == "Aceptada"):
				print("sdhjkhdsjhjks")
				tramitos = reserva.tramos.all()
				for t in tramitos:
					print("ayuda")
					t.asientos_disponibles += reserva.plazas_pedidas
					t.save()
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
				return redirect('registro_conductor')
		else:
			return render(request, 'usuario/registrarme.html', {'form': form})
	else:
		form = Registrationform()
		return render(request, 'usuario/registrarme.html', {'form': form})

def alerta(request):
	request.user.perfil.mensajes=""
	request.user.perfil.save()
	return redirect('home')

def editarperfil(request):
	user = Usuario.objects.get(id=request.user.id)
	#user = us.perfil
	if request.method == 'POST':
		form = EditarPerfil(request.POST)
		print("POST")
		if form.is_valid():
			print("formulario valido")
			if(user.username != form.cleaned_data['username']):
				username = form.cleaned_data['username']
				username_qs = Usuario.objects.filter(username=username)
				if username_qs.exists():
					error = "El nombre de usuario ya está en uso."
					formu = EditarPerfil()
					return render(request,'usuario/editarperfil.html',{'form':form, 'error': error})	
			user.username = form.cleaned_data['username']
			user.email = form.cleaned_data['email']
			user.perfil.numero_telefono = form.cleaned_data['numero_telefono']
			user.perfil.direccion = form.cleaned_data['direccion']
			user.perfil.fumador = form.cleaned_data['fumador']
			user.perfil.profesion = form.cleaned_data['profesion']
			user.save()
			print("guardado")
			#us.save()
			return redirect('ver_perfil')
	else:    	
		data={'username': user.username,
			'email':user.email,
			'numero_telefono':user.perfil.numero_telefono,
			'direccion':user.perfil.direccion,
			'fumador':user.perfil.fumador,
			'profesion':user.perfil.profesion,
		}
		form = EditarPerfil(initial= data)
	return render(request, 'usuario/editarperfil.html', {'form': form})

def editarperfilconduct(request):
	user = Usuario.objects.get(id=request.user.id)
	cond = Conductor.objects.get(usuario=user)
	#cond = user.conductor_set.all()
	#user = us.perfil
	if request.method == 'POST':
		form = EditarPerfilConduct(request.POST)
		print("POST")
		if form.is_valid():
			print("formulario valido")
			if(user.username != form.cleaned_data['username']):
				username = form.cleaned_data['username']
				username_qs = Usuario.objects.filter(username=username)
				if username_qs.exists():
					error = "El nombre de usuario ya está en uso."
					formu = EditarPerfil()
					return render(request,'usuario/editarperfil.html',{'form':form, 'error': error})	
			user.username = form.cleaned_data['username']
			user.email = form.cleaned_data['email']
			user.perfil.numero_telefono = form.cleaned_data['numero_telefono']
			user.perfil.direccion = form.cleaned_data['direccion']
			user.perfil.fumador = form.cleaned_data['fumador']
			user.perfil.profesion = form.cleaned_data['profesion']
			cond.clasedelicencia = form.cleaned_data['clasedelicencia']
			cond.fecha_obtencion = form.cleaned_data['fecha_obtencion']
			cond.car.patente = form.cleaned_data['patente']
			cond.car.marca = form.cleaned_data['marca']
			cond.car.modelo = form.cleaned_data['modelo']
			cond.car.maleta = form.cleaned_data['maleta']
			cond.car.color = form.cleaned_data['color']
			cond.car.Numeroasientos = form.cleaned_data['Numeroasientos']
			cond.car.consumo = form.cleaned_data['consumo']
			cond.car.save()
			cond.save()
			user.save()
			print("guardado")
			#us.save()
			return redirect('ver_perfil')
	else:    	
		data={'username': user.username,
			'email':user.email,
			'numero_telefono':user.perfil.numero_telefono,
			'direccion':user.perfil.direccion,
			'fumador':user.perfil.fumador,
			'profesion':user.perfil.profesion,
			'clasedelicencia':cond.clasedelicencia,
			'fecha_obtencion':cond.fecha_obtencion,
			'patente':cond.car.patente,
    		'marca':cond.car.marca,
    		'modelo':cond.car.modelo,
    		'maleta':cond.car.maleta,
    		'color':cond.car.color,
    		'Numeroasientos':cond.car.Numeroasientos,
    		'consumo':cond.car.consumo,
		}
		form = EditarPerfilConduct(initial= data)
	return render(request, 'usuario/editarperfilconduct.html', {'form': form})

def CambiarContraseña(request):
	if request.method == 'POST':
		form = PasswordChangeForm(user =request.user, data = request.POST)
		if form.is_valid():
			form.save()
			request.user.save()
			update_session_auth_hash(request, form.user)  # Important!
			messages.success(request, 'Tu contraseña ha sido actualizada con éxito!')
			return redirect('ver_perfil')
		else:
			messages.error(request, 'Por favor corregir error.')
	else:
		form = PasswordChangeForm(request.user)
	return render(request, 'usuario/cambiarcontrasena.html', {'form': form})

#para no desplegar Nones
def ingresado(algo):
	return (algo if algo != None else 'No ingresado')
#para no poner true o false
def sino(que):
	return ('Sí' if que else 'No')

@login_required()
def ver_perfil(request):
	info_perfil = []
	us = Usuario.objects.get(id=request.user.id)
	yo = Perfil.objects.get(usuario=us)
	info_perfil.append(ingresado(us.first_name))
	info_perfil.append(ingresado(us.last_name))
	info_perfil.append(ingresado(us.email))
	info_perfil.append(ingresado(yo.numero_telefono))
	info_perfil.append(ingresado(yo.direccion))
	info_perfil.append(ingresado(yo.profesion))
	info_perfil.append(sino(yo.fumador))
	val = Valoracion.objects.all()
	suma = 0
	counter = 0	
	for v in val:
		if v.usuarioEvaluado == us:			
			suma += v.nota
			counter += 1
	if suma > 0:
		promedio = suma/counter
		yo.valoracion = promedio
	info_perfil.append(yo.valoracion)
	yo.save()

	come =[]
	com = Valoracion.objects.filter(usuarioEvaluado=request.user.id)

	for c in com:
		aux = []
		if c.anonimo:
			aux.append('Anónimo')
		else:
			aux.append(c.usuarioEvaluador)
		aux.append(c.nota)
		aux.append(c.comentario)

		come.append(aux)

	paginator = Paginator(come, 10)
	page = request.GET.get('page')
	try:
		comentarios = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		comentarios = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		comentarios = paginator.page(paginator.num_pages)

	cond = us.conductor_set.all()
	for xor in cond:
		info_condu = []
		info_condu.append(ingresado(xor.clasedelicencia))
		info_condu.append(ingresado(xor.fecha_obtencion))
		#auto
		info_condu.append(ingresado(xor.car.patente))
		info_condu.append(ingresado(xor.car.marca))
		info_condu.append(ingresado(xor.car.modelo))
		info_condu.append(ingresado(xor.car.color))
		info_condu.append(ingresado(xor.car.Numeroasientos))
		info_condu.append(ingresado(xor.car.consumo))
		info_condu.append(sino(xor.car.maleta))
		return render(request, 'usuario/mi_perfil_conductor.html', {'perfil': info_perfil, 'perfil_conductor': info_condu, 'comentarios':comentarios})

	return render(request, 'usuario/mi_perfil.html', {'perfil': info_perfil, 'comentarios':comentarios})

@login_required()
def valoracionesPendientesUsuario(request):
	current_user = request.user
	evaluador = Usuario.objects.get(id=current_user.id)
#	print(evaluador)
	porValorar = []
	res = Reserva.objects.all()
	for v in Viaje.objects.all():
		for reserva in res:
			if reserva.tramos.all()[0].viaje == v.id and (reserva.estado == "Por Valorar" or reserva.estado == "Por Valorar Usuario"):
#				print(reserva.usuario)
				aux = []
#				print(v.conductor.usuario)
#				print(reserva.estado)
				aux.append(v.conductor.usuario)
				aux.append(reserva.id)
				aux.append(v.conductor.usuario.id)
				porValorar.append(aux)
	print(porValorar)
	return render(request, 'usuario/valoracionesPendientesUsuario.html',{'porValorar':porValorar})	

#	else:
#		return render(request, 'conductor/valoracionesPendientesConductor')

@login_required()
def vPU(request):
	current_user = request.user
	evaluador = Usuario.objects.get(id=current_user.id)
	valoracion = []
	if request.method == 'POST':
		post = Valoracion()
		post.usuarioEvaluador = evaluador
		evaluado = request.POST.get('conductorEvaluado')
		evaluadoDone = Usuario.objects.get(id=evaluado)
		post.usuarioEvaluado = evaluadoDone
		print(post.usuarioEvaluado)
		post.nota = request.POST.get('nota')
		post.comentario = request.POST.get('comentario')
		post.anonimo = request.POST.get('anon')
		resID = request.POST.get('resID')
		aux = []
		if(post.anonimo == "True"):
			anon = "Anonimo"
			aux.append(anon)
			aux.append(post.nota)
			aux.append(post.usuarioEvaluado)
			aux.append(post.comentario)
			aux.append(post.anonimo)
			valoracion.append(aux)
			print(valoracion)
			post.save()
			res = Reserva.objects.get(id=resID)
			if( res.estado == "Por Valorar Pasajero"):
				res.estado = "Terminada"
				print(res.estado)
				res.save()
			if (res.estado == "Por Valorar"):
				res.estado = "Por Valorar Conductor"
				print(res.estado)
				res.save()
			return HttpResponseRedirect('/valoracionesPendientesUsuario/',{'valoracion':valoracion})
		else:
			aux.append(evaluador)
			aux.append(post.nota)
			aux.append(post.usuarioEvaluado)
			aux.append(post.comentario)
			aux.append(post.anonimo)
			valoracion.append(aux)
			print(valoracion)
			post.save()
			res = Reserva.objects.get(id=resID)
			if( res.estado == "Por Valorar Pasajero"):
				res.estado = "Terminada"
				print(res.estado)					
				res.save()
			if (res.estado == "Por Valorar"):
				res.estado = "Por Valorar Conductor"
				print(res.estado)
				res.save()
			return HttpResponseRedirect('/valoracionesPendientesUsuario/',{'valoracion':valoracion})				

