from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from apps.viaje.forms import *
from apps.viaje.models import Viaje, Tramo, Parada, Reserva
from apps.conductor.models import Conductor
from apps.usuario.models import Usuario
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
import time
import json
from datetime import datetime
from django.http import Http404  

def index(request):
	return render(request, 'usuario/index2.html')

@login_required()
def viaje_view(request):
	print(request.POST.get("cancelar"))
	print("naaaa")
	if request.method == 'POST':
		form = ViajeForm(request.POST)
		try:
			print(form)
		except:
			if(request.POST.get("cancelar") is not None):
				return redirect('cancelar_crear_viaje')
		if request.POST.get("listo"):
			print(request.POST['holiwi'])
			distancias = request.POST['holiwi'].split()
			print("distancias" ,distancias)
			print(request.session['viaje'])
			aux = []
			for i in range(len(distancias)//2):
				aux.append(float(distancias[2*i].replace(',','')))
			try:
				request.session['viaje'].update( {'distancias' : aux} )
			except:
				mensaje = "Ha ocurrido un error, intenta publicar tu viaje nuevamente"
				form = ViajeForm()
				return render(request,'viaje/crear2.html',{'form':form, 'error': mensaje})
			return viaje_listo(request)
		elif form.is_valid():
			#viaje = Viaje()
			#viaje.fecha = form.cleaned_data['fecha']
			#viaje.estado = "Registrado"
			#viaje.porta_maleta = form.cleaned_data['porta_maleta']
			#viaje.mascotas = form.cleaned_data['mascotas']
			#viaje.tarifaPreferencias = form.cleaned_data['tarifapreferencias']
			#viaje.plazas_disponibles = form.cleaned_data['plazas_disponibles']
			#current_user = request.user
			#u = Usuario.objects.get(id=current_user.id)
			#viaje.conductor = u.conductor_set.all()[0]
			#viaje.save()
			aux2 = dict()
			aux2['fecha'] = form.cleaned_data['fecha'].strftime("%d/%m/%Y")
			aux2['porta_maleta'] = form.cleaned_data['porta_maleta']
			aux2['mascotas'] = form.cleaned_data['mascotas']
			aux2['tarifaPreferencias'] = form.cleaned_data['tarifapreferencias']
			aux2['plazas_disponibles'] = form.cleaned_data['plazas_disponibles']
			#current_user = request.user
			#u = Usuario.objects.get(id=current_user.id)
			#viaje.conductor = u.conductor_set.all()[0]
			aux = []
			#request.session['viaje'] = viaje.id
			#print(request.session['viaje'])
			#Paradas en aux
			aux.append([form.cleaned_data['fecha'].strftime("%d/%m/%Y"), form.cleaned_data['hora_origen'].strftime("%H:%M"), request.POST['origen'].split(',')[0].replace(',',''), request.POST['origen']])
			aux.append([form.cleaned_data['fecha_destino'].strftime("%d/%m/%Y"), form.cleaned_data['hora_destino'].strftime("%H:%M"), request.POST['destino'].split(',')[0].replace(',',''), request.POST['destino']])
			#request.session['paradas'] = aux
			aux2['paradas'] = aux
			request.session['viaje'] = aux2
			if request.POST.get("agregar"):
				return redirect('paradas')
			elif request.POST.get("publicar"):
				return viaje_ver(request)

		else:
			print("Invalido")
			print(form)
			return render(request,'viaje/crear2.html',{'form':form})
	else:
		form = ViajeForm()
		return render(request,'viaje/crear2.html',{'form':form})

@login_required()
def viaje_list(request):
	viaje = Viaje.objects.all()
	contexto = {'viajes':viaje}
	return render(request, 'viaje/viaje_list.html', contexto)

#Funcion intermedia que solo crea paradas y tramos del viaje
@login_required()
def viaje_listo(request):
	print("hola que tal como estas todo bien ", request.session['viaje'])
	try:
		hola = request.session['viaje']
		paradas = request.session['viaje']['paradas']
	except:
		raise Http404
	viaje = Viaje()
	viaje.fecha = datetime.strptime(request.session['viaje']['fecha'], "%d/%m/%Y")
	viaje.estado = "Registrado"
	viaje.porta_maleta = request.session['viaje']['porta_maleta']
	viaje.mascotas = request.session['viaje']['mascotas']
	viaje.tarifaPreferencias = request.session['viaje']['tarifaPreferencias']
	viaje.plazas_disponibles = request.session['viaje']['plazas_disponibles']
	current_user = request.user
	u = Usuario.objects.get(id=current_user.id)
	viaje.conductor = u.conductor_set.all()[0]
	viaje.save()
	for i in range(len(paradas)-1):
		if(i==0):
			par1 = Parada()
			par1.nombre = paradas[i][2]
			par1.direccion = paradas[i][3]
			par1.save()

			par2 = Parada()
			par2.nombre = paradas[i+1][2]
			par2.direccion = paradas[i+1][3]
			par2.save()
		else:
			par1 = par2
			par2 = Parada()
			par2.nombre = paradas[i+1][2]
			par2.direccion = paradas[i+1][3]
			par2.save()

		tramo = Tramo()
		tramo.orden_en_viaje  = i
		tramo.hora_salida = paradas[i][1]
		tramo.hora_llegada = paradas[i+1][1]
		tramo.fecha = datetime.strptime(paradas[i][0], "%d/%m/%Y")
		tramo.asientos_disponibles = request.session['viaje']['plazas_disponibles']
		tramo.origen = par1
		tramo.destino = par2
		tramo.distancia = request.session['viaje']['distancias'][i]
		tramo.viaje = viaje.id
		tramo.save()
		print("He guardado un tramito")
		viaje.tramos.add(tramo)
	viaje.save()
	return success(request,viaje.id)	
	#viaje  = Viaje.objects.get(id = pk)
	#aux = request.session['paradas']
	#aux.sort()
	#for i in range(0,len(aux)-1):
	#	if(i==0):
	#		par1 = Parada()
	#		par1.nombre = aux[i][2]
	#		par1.direccion = aux[i][3]
	#		par1.save()

	#		par2 = Parada()
	#		par2.nombre = aux[i+1][2]
	#		par2.direccion = aux[i+1][3]
	#		par2.save()
	#	else:
	#		par1 = par2
	#		par2 = Parada()
	#		par2.nombre = aux[i+1][2]
	#		par2.direccion = aux[i+1][3]
	#		par2.save()

	#	tramo = Tramo()
	#	tramo.orden_en_viaje  = i
	#	tramo.hora_salida = aux[i][1]
	#	tramo.hora_llegada = aux[i+1][1]
	#	tramo.fecha = aux[i][0]
	#	tramo.asientos_disponibles = viaje.plazas_disponibles
	#	tramo.origen = par1
	#	tramo.destino = par2
	#	tramo.viaje = pk
	#	tramo.save()

	#	viaje.tramos.add(tramo)
	#aux = []
	#viaje.save()
	#return redirect("mapa_ejemplo")

@login_required()
def Viajelist(request):
	lista = []
	current_user = request.user
	u = Usuario.objects.get(id=current_user.id)
	conductor = u.conductor_set.all()[0]
	res = Reserva.objects.all()
	for v in Viaje.objects.all():
		if v.conductor == conductor:
			aux = []
			resHechas = 0
			for reserva in res:
				if reserva.tramos.all()[0].viaje == v.id and reserva.estado == "Aceptada" :
					resHechas+=reserva.plazas_pedidas
			tramito = v.tramos.all().order_by('orden_en_viaje')
			aux.append(v)
			aux.append(tramito[0])
			aux.append(tramito[len(tramito)-1])
			print(v.fecha)
			aux.append(str(v.fecha).split()[0])
			aux.append(len(tramito))
			aux.append(v.plazas_disponibles)
			aux.append(resHechas)
			lista.append(aux)
	return render(request, 'viaje/viaje_list.html', {'viajes':lista})

@login_required()
def success(request, pk):
	print("success")
	viaje  = Viaje.objects.get(id = pk)
	return render(request, 'viaje/listo.html', {'id': pk})	

#Funcion que se conecta con agregar paradas, se llama asi misma hasta que se publique el viaje o se aprete cancelar
@login_required()
def viaje_paradas(request):
	print("hola que tal como estas todo bien ", request.session['viaje'])
	try:
		if(request.POST.get("cancelar") is not None):
			return redirect('cancelar_crear_viaje')
		hola = request.session['viaje']
		hola2 = request.session['viaje']['paradas']
	except:
		raise Http404  
	if(request.method == 'POST'):
		form = ParadasForm(request.POST)
		if request.POST.get('agregar'):
			form = ParadasForm()
			aux = dict()
			aux = request.session['viaje']
			request.session['viaje'] = aux
			return render(request,'viaje/paradas.html',{'form':form})
		if request.POST.get("listo"):
			return viaje_ver(request)
		elif form.is_valid():
			aux = []
			aux = request.session['viaje']['paradas']
	#	if form.is_valid():
	#		viaje = Viaje.objects.get(id = pk)
	#		fo = viaje.fecha.strftime("%d/%m/%Y")
			fo = request.session['viaje']['fecha']
			fd = aux[1][0]
			fp = form.cleaned_data['fecha'].strftime("%d/%m/%Y")
			ho = aux[0][1]
			hd =  aux[1][1]
			hp = form.cleaned_data['hora'].strftime("%H:%M")
	#		print("hora ",hp)
	#		print("hora origen ",ho)
	#		print("hora destino ",hd)
	#		print(hp > hd, "hora parada mayor que hora destino")
			if (fp < fo or fd < fp or (fo == fp and hp <= ho) or (fd == fp and hd <= hp)):
				error = "Fecha y hora de la parada deben ser consistentes con las fechas y horas de origen y destino."
				form = ParadasForm()
				return render(request,'viaje/paradas.html',{'form':form, 'error': error})
			elif request.POST.get("agregar2"):
				print("Agregue una parada")
				direccion = str(request.POST['direccion'])
				aux.append([fp, hp,direccion.split(',')[0].replace(',',''), direccion])
				aux2 = dict()
				aux2 = request.session['viaje']
				request.session['viaje'] = aux2
				request.session['viaje']['paradas'] = aux
				form = ParadasForm()
				return render(request,'viaje/paradas.html',{'form':form})
			elif request.POST.get("publicar2"):
				direccion = str(request.POST['direccion'])
				aux.append([fp, hp,direccion.split(',')[0].replace(',',''), direccion])
				request.session['viaje']['paradas'] = aux
				return viaje_ver(request)
			else:
				error = "Ha ocurrido un error inesperado. Disculpe por las molestias"
				form = ParadasForm()
				return render(request,'viaje/paradas.html',{'form':form, 'error': error})
	#	elif request.POST.get("publicar"):
	#		request.session['paradas'] = aux
	#		return viaje_listo(request, pk)
		else:
			form = ParadasForm()
			return render(request,'viaje/paradas.html',{'form':form})
	form = ParadasForm()
	return render(request,'viaje/paradas.html',{'form':form})

#Funcion que se encarga de pasarle todos las paradas del viaje al mapa para mostrar el viaje
@login_required()
def viaje_ver(request):
	print("viaje_ver ", request.session['viaje'])
	try:
		hola = request.session['viaje']
		paradas = request.session['viaje']['paradas']
	except:
		raise Http404  
	if request.method == "POST":
		if request.POST.get("listo"):
			print("listo")
			distancias = request.POST['holiwi'].split()
			print(distancias)
			aux = []
			for i in range(len(distancias)//2):
				aux.append(float(distancias[2*i].replace(',','')))
			request.session['viaje'].update( {'distancias' : aux} )
			print(request.session['viaje'])
			return viaje_listo(request)
		elif request.POST.get("publicar2") or request.POST.get("publicar"):
			print("publicar")
			jotason = []
			paradas.sort()
			for p in paradas:
				jotason.append(p[3])
			json_cities = json.dumps(jotason)
			request.session['viaje'] = hola
			request.session['viaje']['paradas'] = paradas
			print("paradas", paradas)
			print("request", request)
			return render (request, 'viaje/ejemplo.html', {"city_array" : json_cities, "paradas": paradas, "max": len(paradas)-1})
	else:
		raise Http404  
		#aux = request.POST['holiwi'].split()
		#viaje  = Viaje.objects.get(id = pk)
		#tramitos = viaje.tramos.all()
		#if(len(aux)//2 == len(tramitos)):
		#	for i in range(len(tramitos)):
		#		tramitos[i].distancia = float(aux[2*i])
		#		tramitos[i].save()
		#	return success(request,pk)	
		#else:
		#	return success(request,pk)
	#else:
		#paradas = []
		#viaje  = Viaje.objects.get(id = pk)
		#tramitos = viaje.tramos.all()
		#ultimo = len(tramitos)
		#for i in range(len(tramitos)):
		#	if i != len(tramitos)-1:
		#		paradas.append(tramitos[i].origen.direccion)
		#	else :
		#		paradas.append(tramitos[i].origen.direccion)
		#		paradas.append(tramitos[i].destino.direccion)
		#print(paradas)
		#json_cities = json.dumps(paradas)
		#print(json_cities)
		#return render (request, 'viaje/ejemplo.html', {"city_array" : json_cities})

@login_required()
def buscar_viaje(request):
	print("shdjkhfjkshkd", request.method)
	if request.method == 'GET':
		form = BuscarForm()
		return render(request,'viaje/buscarviaje.html',{'form': form})
	else:
		print("Holiwi, soy un post")
		resultado = []
		form = BuscarForm(request.POST)
		if form.is_valid():
			f =  form.cleaned_data['fecha']
			s = request.POST['origen'].split(',')[0].replace(",","")
			u = request.POST['destino'].split(',')[0].replace(",","")
			viaje  = Viaje.objects.filter()
			#se revisan todos lo viajes
			origen = False
			destino = False
			print(viaje)
			for v in viaje:
				origen = False
				destino = False
				distancia = 0;
				tramitos = v.tramos.all()
				asientos=v.plazas_disponibles
				print(tramitos)
				print(v.tarifaPreferencias)
				#se revisan los tramos del viaje
				for t in tramitos:
					print(t)
					print(t.distancia)
					print(origen)
					print(t.origen.nombre , s)
					print(t.destino.nombre, u)
					print(t.fecha,f)
					print(t.fecha == f)
					#Como el origen se debe encontrar primero y no sirve que la ultima parada del viaje coincida con este, solo se revisa la primera parada del tramo
					if(t.origen.nombre == s and t.fecha == f):
						distancia = 0
						origen = True
						print(origen)
					#solo importa ver si el destino existe cuando ya se encontró el origen
					if(origen):
						distancia += float(t.distancia)
						
						if(asientos>t.asientos_disponibles):
							asientos=t.asientos_disponibles

						#si es que los asientos disponibles son 0 en el camino, el viaje no sirve. Pero debo seguir revisando ya que se podria pasar por ahi de nuevo
						# y alli podrian haber asientos disponibles
						if(t.asientos_disponibles == 0):
							origen = False
						elif(t.destino.nombre == u):
							destino = True
							break
				if(origen and destino):
					resultado.append([v,tramitos[0], tramitos[len(tramitos)-1],distancia*v.tarifaPreferencias, len(tramitos),asientos])
			if(resultado):
				return render(request, 'viaje/buscar2.html', {'viajes':resultado, 'origen':s, 'destino':u})
			else:
				return render(request,'viaje/buscar2.html',{'viajes':resultado, 'origen':s, 'destino':u})
		else:
			return render(request,'viaje/buscarviaje.html',{'form': form})
def tiene_reservas(pk):
	aux = Viaje.objects.get(id = pk)
	tramitos = aux.tramos.all()
	for i in tramitos:
		try:
			reservas = i.reservas.all()
			for r in reservas:
				if(r.estado == "Por Aprobar" or r.estado == "Aceptada"):
					return True
		except:
			continue
	return False

@login_required()
def error1(request):
	return render(request, 'viaje/error1.html', {})

@login_required()
def viaje_details(request, pk):
	viajes=[]
	paradas = []
	trams = []
	viaje  = Viaje.objects.get(id = pk)
	tramitos = viaje.tramos.all()
	for tr in tramitos:
		trams.append([tr,viaje.plazas_disponibles-tr.asientos_disponibles])
	ultimo = len(tramitos)
	print(tramitos)
	print(trams)
	if request.method == 'GET':
		aux = Viaje.objects.get(id = pk)
		tramitos = aux.tramos.all().order_by('orden_en_viaje')
		for i in tramitos:
			print(i.orden_en_viaje)
			print("origen: ", i.origen.nombre)
		viajes.append(aux)
		viajes.append(trams)
		viajes.append(str(aux.fecha).split()[0])

	for i in range(len(tramitos)):
		if i != len(tramitos)-1:
			paradas.append(tramitos[i].origen.direccion)
		else :
			paradas.append(tramitos[i].origen.direccion)
			paradas.append(tramitos[i].destino.direccion)
	json_cities = json.dumps(paradas)
	#Caso en que un conductor este viendo sus viajes
	try:
		current_user = request.user
		u = Usuario.objects.get(id=current_user.id)
		u.conductor_set.all()[0]
		r=Reserva.objects.all()
		reservas = []
		for reserva in r:
			if (reserva.estado == "Por Aprobar"):
				tramosreserva = reserva.tramos.all()
				aux = []
				print(reserva.tramos.all()[0].viaje == int(pk))
				if reserva.tramos.all()[0].viaje == int(pk):
					aux.append(reserva.id)
					aux.append(reserva.plazas_pedidas)
					aux.append(tramosreserva[0].origen.nombre)
					aux.append(tramosreserva[len(tramosreserva)-1].destino.nombre)
					aux.append(reserva.precio)
					aux.append(reserva.estado)
					reservas.append(aux)
					print("despues de todo.id")
		return render(request, 'viaje/viaje_details.html', {'viajes':viajes, 'paradas':json_cities, 'ultimo':ultimo,'reservas':reservas})
		#Caso en que un pasajero quiera ver detalles de un viaje buscado
	except:
		return render(request, 'viaje/viaje_details_buscar.html',{'viajes':viajes, 'paradas':json_cities, 'ultimo':ultimo})
	



@login_required()
def editarviaje(request,idviaje):
	if(tiene_reservas(idviaje)):
		return redirect('cancelar_editar_error')
	viaje = Viaje.objects.get(id=idviaje)
	print(viaje)
	tramitos = viaje.tramos.all()
	print("tramitos", tramitos)
	i = 0
	for t in tramitos:
		print(i)
		print(t)
		print(t.origen.nombre)
		print(t.destino.nombre)
		i +=1
	print(len(tramitos)-1)
	if request.method == 'GET':
		form = EditarViajeForm()
	else:
		form = EditarViajeForm(request.POST)
		if form.is_valid():
			#viaje.fecha = form.cleaned_data['fecha']
			#viaje.estado = "Registrado"
			#viaje.porta_maleta = form.cleaned_data['porta_maleta']
			#viaje.mascotas = form.cleaned_data['mascotas']
			#viaje.tarifaPreferencias = form.cleaned_data['tarifapreferencias']
			#viaje.plazas_disponibles = form.cleaned_data['plazas_disponibles']
			#tramitos[0].origen.direccion = form.cleaned_data['origen']
			pks = []
			for t in tramitos:
				pks.append(t.id)

			par1 = Parada()
			par1.nombre = request.POST['origen'].split(',')[0].replace(',','')
			par1.direccion = request.POST['origen']
			par1.save()

			par2 = Parada()
			par2.nombre = request.POST['destino'].split(',')[0].replace(',','')
			par2.direccion = request.POST['destino']
			par2.save()
			if len(tramitos)==1:
				tramo1 = Tramo()
				tramo1.orden_en_viaje  = 0
				tramo1.hora_salida = form.cleaned_data['hora_origen']
				tramo1.hora_llegada = form.cleaned_data['hora_destino']
				tramo1.fecha = form.cleaned_data['fecha_destino']
				tramo1.asientos_disponibles = 4
				tramo1.origen = par1
				tramo1.destino = par2
				tramo1.distancia = 0
				tramo1.viaje = viaje.id
				tramo1.save()
				viaje.porta_maleta=form.cleaned_data['porta_maleta']
				viaje.silla_niños=form.cleaned_data['silla_niños']
				viaje.mascotas=form.cleaned_data['mascotas']
				viaje.tarifaPreferencias=form.cleaned_data['tarifapreferencias']
				viaje.max_personas_atras=form.cleaned_data['max_personas_atras']
				viaje.fecha = form.cleaned_data['fecha']
				viaje.tramos.clear()
				viaje.tramos.add(tramo1)
				viaje.save()
			else:	
				tramo1 = Tramo()
				tramo1.orden_en_viaje  = 0
				tramo1.hora_salida = form.cleaned_data['hora_origen']
				tramo1.hora_llegada = tramitos[0].hora_llegada
				tramo1.fecha = form.cleaned_data['fecha']
				tramo1.asientos_disponibles = 4
				tramo1.origen = par1
				tramo1.destino = tramitos[0].destino
				tramo1.distancia = 0
				tramo1.viaje = viaje.id
				tramo1.save()
				pks[0] = tramo1.id

				tramo2 = Tramo()
				tramo2.orden_en_viaje  = len(tramitos)-1
				tramo2.hora_salida = tramitos[len(tramitos)-1].hora_salida
				tramo2.hora_llegada = form.cleaned_data['hora_destino']
				tramo2.fecha =  form.cleaned_data['fecha_destino']
				#if(form.cleaned_data['fecha_destino']<tramitos[len(tramitos)-2].fecha):
				#	messages.warning(request, 'La fecha de llegada es menor a la fecha de la parada anterior')
				#	render(request, 'viaje/editarviaje.html', {'form':form})
				tramo2.asientos_disponibles = 4
				tramo2.origen = tramitos[len(tramitos)-1].origen
				tramo2.destino = par2
				tramo2.distancia = 0
				tramo2.viaje = viaje.id
				tramo2.save()
				pks[len(tramitos)-1] = tramo2.id
				viaje.tramos.clear()
				i = 0
				for pk in pks:
					tramon = Tramo.objects.get(id = pk)
					print("tramo ", i)
					print("origen : ", tramon.origen.nombre , " destino : ", tramon.destino.nombre)
					viaje.tramos.add(tramon)
					i +=1
				viaje.porta_maleta=form.cleaned_data['porta_maleta']
				viaje.silla_niños=form.cleaned_data['silla_niños']
				viaje.mascotas=form.cleaned_data['mascotas']
				viaje.tarifaPreferencias=form.cleaned_data['tarifapreferencias']
				viaje.max_personas_atras=form.cleaned_data['max_personas_atras']
				viaje.fecha = form.cleaned_data['fecha']
				viaje.save()
			return redirect('viaje_list')
		return render(request,'viaje/editarviaje.html',{'form':form})
	return render(request, 'viaje/editarviaje.html', {'form':form})

@login_required()
def confirmarCan(request, pk):
	return render(request, 'viaje/confirmarCanc.html', {'id' : pk})

@login_required()
def cancelar(request, pk):
	if(tiene_reservas(pk)):
		return redirect('cancelar_editar_error')
	viaje = Viaje.objects.get(id=pk)
	tramitos = viaje.tramos.all()
	i = len(tramitos)-1
	while i>=0:
		tram=tramitos[i]
		tram.destino.delete()
		if i == 0:
			tram.origen.delete()
		tram.delete()
		i=i-1
	viaje.delete()
	return Viajelist(request)

@login_required()
def realizar_reservas(request):
	if request.method == 'GET':
		idviaje=request.GET['idviaje']
		Origen=request.GET['Origen']
		Destino=request.GET['Destino']
		viaje=Viaje.objects.get(id=idviaje)
		tramos = []
		resPedidas = []
		distancia =0
		aux=False
		tramitos=viaje.tramos.all()
		asientos=tramitos[0].asientos_disponibles
		for tr in tramitos:
			if aux:
				tramos.append([tr,viaje.plazas_disponibles-tr.asientos_disponibles])
				distancia+=tr.distancia
				if tr.asientos_disponibles<asientos:
					asientos=asientos_disponibles
			if tr.origen.nombre == Origen and aux==False:
				tramos.append([tr,viaje.plazas_disponibles-tr.asientos_disponibles])
				distancia+=tr.distancia
				if tr.asientos_disponibles<asientos:
					asientos=asientos_disponibles
				aux=True		
			if tr.destino.nombre == Destino:
				ultimo=tr
				if tr.asientos_disponibles<asientos:
					asientos=asientos_disponibles
				break
		precio=distancia*viaje.tarifaPreferencias
		v=[idviaje,precio,distancia,asientos]
		print(tramos)
	return render(request, 'viaje/realizar_reservas.html', {'viaje':v , 'tramos':tramos,'ultimo':ultimo})

@login_required()
def guardar_reservas(request):
	if request.method == 'GET':
		reserva = Reserva()
		asientos=request.GET['asientos']
		origen=request.GET['origen']
		idviaje=request.GET['idviaje']
		destino=request.GET['destino']
		precio=request.GET['precio']
		pasajero=request.user
		viaje=Viaje.objects.get(id=idviaje)
		tramitos = viaje.tramos.all()
		print(tramitos)
		print(origen)
		print(destino)
		aux=False
		reserva.precio=float(precio.replace(',','.'))
		reserva.plazas_pedidas=asientos
		reserva.estado="Por Aprobar"
		reserva.usuario=pasajero
		reserva.save()
		v = Viaje.objects.get(id=idviaje)
		v.conductor.reservas_por_aprobar += 1
		v.conductor.save()
		for tram in tramitos:
			if aux:
				#tram.asientos_disponibles-=int(asientos)
				#tram.save()
				print(tram.asientos_disponibles)
				reserva.tramos.add(tram)	
				aux=True

			if tram.origen.nombre == origen and aux==False:
				#tram.asientos_disponibles-=int(asientos)
				#tram.save()
				reserva.tramos.add(tram)	
				aux=True		
			
			if tram.destino.nombre == destino:
				break
		reserva.save()

		if v.conductor.autoaceptar_reservas:#Aceptar automaticamente
			print("Autoaceptando")
			aceptarreserva = True
			for tram in tramitos:#revisar disponibilidad de cada tramo
				if int(asientos) > tram.asientos_disponibles:
					aceptarreserva = False
					print("No autoaceptado")
					break
			if aceptarreserva:
				for tram in tramitos:
					tram.asientos_disponibles -= int(asientos)
					tram.save()
				reserva.estado="Aceptada"
				reserva.save()
				v.conductor.reservas_por_aprobar -= 1
				v.conductor.save()
				print("Autoaceptado")

	return render(request, 'usuario/index.html')

@login_required()
def cancelar_crear_viaje(request):
	request.session['viaje'] = ''
	return redirect('home')
@login_required()
def confirmarCanReservaConductor(request, pk):
	return render(request, 'viaje/confirmarCanReservaConductor.html', {'id' : pk})

@login_required()
def cancelarReservaConductor(request, pk):
	reservas = Reserva.objects.filter(id=pk)
	reserva = reservas[0]
	if(reserva.estado == "Por Aprobar"):
		reserva.estado = "Rechazada"
		print(reserva.estado)
		reserva.save()
		exitocancelarreservaconductor = True
		return render(request, 'viaje/cancelarReservaConductor.html', {'exitocancelarreservaconductor' : exitocancelarreservaconductor})
	else:
		exitocancelarreservaconductor = False
		return render(request, 'viaje/cancelarReservaConductor.html', {'exitocancelarreservaconductor' : exitocancelarreservaconductor})

@login_required()
def confirmarAceptarReservaConductor(request, pk):
	return render(request, 'viaje/confirmarAceptarReservaConductor.html', {'id' : pk})

@login_required()
def aceptarReservaConductor(request, pk):
	reservas = Reserva.objects.filter(id=pk)
	reserva = reservas[0]
	tramosreserva = reserva.tramos.all()
	for t in tramosreserva:
		if (reserva.plazas_pedidas <= t.asientos_disponibles):
			print(t.asientos_disponibles)
			checked = True
			print(checked)
		else:
			exitoaceptarreservaconductor = False
			return render(request, 'viaje/aceptarReservaConductor.html', {'exitoaceptarreservaconductor' : exitoaceptarreservaconductor})
	if (checked == True):
		for i in tramosreserva:
			print("Pre resta", i.asientos_disponibles)
			i.asientos_disponibles -= reserva.plazas_pedidas
			print("Post resta", i.asientos_disponibles)
			i.save()
		reserva.estado = "Aceptada"
		reserva.save()
		exitoaceptarreservaconductor = True
		return render(request, 'viaje/aceptarReservaConductor.html', {'exitoaceptarreservaconductor' : exitoaceptarreservaconductor})
	else:
		exitoaceptarreservaconductor = False
		return render(request, 'viaje/aceptarReservaConductor.html', {'exitoaceptarreservaconductor' : exitoaceptarreservaconductor})
