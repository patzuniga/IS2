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
from datetime import datetime
import pytz

def index(request):
	return render(request, 'usuario/index2.html')

@login_required()
def viaje_view(request):
	print(request.POST.get("cancelar"))
	if request.method == 'POST':
		form = ViajeForm(request.POST)
		try:
			print(form)
		except:
			if(request.POST.get("cancelar") is not None):
				return redirect('cancelar_crear_viaje')
		if request.POST.get("listo"):
			distancias = request.POST['holiwi'].split()
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
			aux2 = dict()
			aux2['fecha'] = form.cleaned_data['fecha'].strftime("%d/%m/%Y")
			aux2['porta_maleta'] = form.cleaned_data['porta_maleta']
			aux2['mascotas'] = form.cleaned_data['mascotas']
			aux2['tarifaPreferencias'] = form.cleaned_data['tarifapreferencias']
			aux2['plazas_disponibles'] = form.cleaned_data['plazas_disponibles']
			aux = []
			aux.append([form.cleaned_data['fecha'].strftime("%d/%m/%Y"), form.cleaned_data['hora_origen'].strftime("%H:%M"), request.POST['origen'].split(',')[0].replace(',',''), request.POST['origen']])
			aux.append([form.cleaned_data['fecha_destino'].strftime("%d/%m/%Y"), form.cleaned_data['hora_destino'].strftime("%H:%M"), request.POST['destino'].split(',')[0].replace(',',''), request.POST['destino']])
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
		viaje.tramos.add(tramo)
	viaje.save()
	return success(request,viaje.id)	

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
				if reserva.tramos.all()[0].viaje == v.id and reserva.estado == "Aprobada" :
					resHechas+=reserva.plazas_pedidas
			tramito = v.tramos.all().order_by('orden_en_viaje')
			aux.append(v)
			aux.append(tramito[0])
			aux.append(tramito[len(tramito)-1])
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
			fo = request.session['viaje']['fecha']
			fd = aux[1][0]
			fp = form.cleaned_data['fecha'].strftime("%d/%m/%Y")
			ho = aux[0][1]
			hd =  aux[1][1]
			hp = form.cleaned_data['hora'].strftime("%H:%M")
			if (fp < fo or fd < fp or (fo == fp and hp <= ho) or (fd == fp and hd <= hp)):
				error = "Fecha y hora de la parada deben ser consistentes con las fechas y horas de origen y destino."
				form = ParadasForm()
				return render(request,'viaje/paradas.html',{'form':form, 'error': error})
			elif request.POST.get("agregar2"):
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
			distancias = request.POST['holiwi'].split()
			aux = []
			for i in range(len(distancias)//2):
				aux.append(float(distancias[2*i].replace(',','')))
			request.session['viaje'].update( {'distancias' : aux} )
			print(request.session['viaje'])
			return viaje_listo(request)
		elif request.POST.get("publicar2") or request.POST.get("publicar"):
			jotason = []
			paradas.sort()
			for p in paradas:
				jotason.append(p[3])
			json_cities = json.dumps(jotason)
			request.session['viaje'] = hola
			request.session['viaje']['paradas'] = paradas
			return render (request, 'viaje/ejemplo.html', {"city_array" : json_cities, "paradas": paradas, "max": len(paradas)-1})
	else:
		raise Http404  

@login_required()
def buscar_viaje(request):
	if request.method == 'GET':
		form = BuscarForm()
		return render(request,'viaje/buscarviaje.html',{'form': form})
	else:
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
				tramitos = v.tramos.all().order_by('orden_en_viaje')
				asientos=v.plazas_disponibles
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
				if(r.estado == "Por Aprobar" or r.estado == "Aprobada"):
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
	if request.method == 'GET':
		aux = Viaje.objects.get(id = pk)
		tramitos = aux.tramos.all().order_by('orden_en_viaje')
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
		reservasdecididasaceptadas = []
		reservasdecididasrechazadas = []
		for reserva in r:
			if (reserva.estado == "Por Aprobar"):
				tramosreserva = reserva.tramos.all()
				aux = []
				if reserva.tramos.all()[0].viaje == int(pk):
					aux.append(reserva.id)
					aux.append(reserva.plazas_pedidas)
					aux.append(tramosreserva[0].origen.nombre)
					aux.append(tramosreserva[len(tramosreserva)-1].destino.nombre)
					aux.append(reserva.precio)
					aux.append(reserva.estado)
					aux.append(reserva.usuario)
					reservas.append(aux)
			if (reserva.estado == "Aprobada"):
				tramosreserva = reserva.tramos.all()
				aux = []
				if reserva.tramos.all()[0].viaje == int(pk):
					aux.append(reserva.id)
					aux.append(reserva.plazas_pedidas)
					aux.append(tramosreserva[0].origen.nombre)
					aux.append(tramosreserva[len(tramosreserva)-1].destino.nombre)
					aux.append(reserva.precio)
					aux.append(reserva.estado)
					aux.append(reserva.usuario)
					reservasdecididasaceptadas.append(aux)
			if (reserva.estado == "Rechazada"):
				tramosreserva = reserva.tramos.all()
				aux = []
				if reserva.tramos.all()[0].viaje == int(pk):
					aux.append(reserva.id)
					aux.append(reserva.plazas_pedidas)
					aux.append(tramosreserva[0].origen.nombre)
					aux.append(tramosreserva[len(tramosreserva)-1].destino.nombre)
					aux.append(reserva.precio)
					aux.append(reserva.estado)
					aux.append(reserva.usuario)
					reservasdecididasrechazadas.append(aux)		
		return render(request, 'viaje/viaje_details.html', {'viajes':viajes, 'paradas':json_cities, 'ultimo':ultimo,'reservas':reservas, 'reservasdecididasaceptadas':reservasdecididasaceptadas, 'reservasdecididasrechazadas': reservasdecididasrechazadas})
		#Caso en que un pasajero quiera ver detalles de un viaje buscado
	except:
		return render(request, 'viaje/viaje_details_buscar.html',{'viajes':viajes, 'paradas':json_cities, 'ultimo':ultimo})

@login_required()
def editarviaje(request,idviaje):
	lista=[]
	if(tiene_reservas(idviaje)):
		return redirect('cancelar_editar_error')
	viaje = Viaje.objects.get(id=idviaje)
	tramitos = viaje.tramos.all()
	if request.method == 'GET':
		data= {'fecha':viaje.fecha, 
				'porta_maleta':viaje.porta_maleta,
				'silla_niños':viaje.silla_niños,
				'mascotas':viaje.mascotas ,
				'tarifapreferencias':viaje.tarifaPreferencias,
				'asientos_disponibles':viaje.plazas_disponibles,
				'hora_origen':tramitos[0].hora_salida, 
				'fecha_destino':tramitos[len(tramitos)-1].fecha, 
				'hora_destino':tramitos[len(tramitos)-1].hora_llegada,
				'destino':tramitos[len(tramitos)-1].destino.nombre,
				'origen':tramitos[0].origen.nombre}
		form = EditarViajeForm(initial=data)
		return render(request, 'viaje/editarviaje.html', {'form':form})
	else:
		form = EditarViajeForm(request.POST)
		if request.POST.get("listo"):
			return Editarlisto(request,idviaje)
		if form.is_valid():
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

			f1 = form.cleaned_data['fecha']
			h1 = form.cleaned_data['hora_origen']
			f2 = form.cleaned_data['fecha_destino']
			h2 = form.cleaned_data['hora_destino']
			tz = pytz.timezone('Chile/Continental')
			actual = datetime.strptime(datetime.now(tz=tz).strftime("%d/%m/%Y %H:%M:%S") , "%d/%m/%Y %H:%M:%S")
			fecha_origen = datetime.strptime(datetime.combine(f1,h1).strftime("%d/%m/%Y %H:%M:%S") , "%d/%m/%Y %H:%M:%S")
			fecha_destino = datetime.strptime(datetime.combine(f2,h2).strftime("%d/%m/%Y %H:%M:%S") , "%d/%m/%Y %H:%M:%S")
			if(actual > fecha_origen or actual > fecha_destino):
				error = "Fecha de origen y destino no pueden ser menores a la fecha actual."
				form = EditarViajeForm()
				return render(request,'viaje/editarviaje.html',{'form':form, 'error': error})	
			if (fecha_destino < fecha_origen):
				error = "Fecha y hora de termino deben ser mayores a la fecha y hora de inicio."
				form = EditarViajeForm()
				return render(request,'viaje/editarviaje.html',{'form':form, 'error': error})	

			if len(tramitos)==1:
				tramo1 = Tramo()
				tramo1.orden_en_viaje  = 0
				tramo1.hora_salida = form.cleaned_data['hora_origen']
				tramo1.hora_llegada = form.cleaned_data['hora_destino']
				tramo1.fecha = form.cleaned_data['fecha_destino']
				tramo1.asientos_disponibles = form.cleaned_data['asientos_disponibles'] 
				tramo1.origen = par1
				tramo1.destino = par2
				tramo1.distancia = 0
				tramo1.viaje = viaje.id
				tramo1.save()
				viaje.porta_maleta=form.cleaned_data['porta_maleta']
				viaje.silla_niños=form.cleaned_data['silla_niños']
				viaje.mascotas=form.cleaned_data['mascotas']
				viaje.tarifaPreferencias=form.cleaned_data['tarifapreferencias']
				viaje.plazas_disponibles=form.cleaned_data['asientos_disponibles']
				viaje.fecha = form.cleaned_data['fecha']
				viaje.tramos.clear()
				viaje.tramos.add(tramo1)
				viaje.save()
			else:	
				if(form.cleaned_data['fecha_destino']<tramitos[len(tramitos)-2].fecha):
					error = "La fecha de llegada es menor a la fecha de la parada anterior."
					form = EditarViajeForm()
					return render(request,'viaje/editarviaje.html',{'form':form, 'error': error})	
				tramo1 = Tramo()
				tramo1.orden_en_viaje  = 0
				tramo1.hora_salida = form.cleaned_data['hora_origen']
				tramo1.hora_llegada = tramitos[0].hora_llegada
				tramo1.fecha = form.cleaned_data['fecha']
				tramo1.asientos_disponibles = form.cleaned_data['asientos_disponibles'] 
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
				
				

				tramo2.asientos_disponibles = form.cleaned_data['asientos_disponibles'] 
				tramo2.origen = tramitos[len(tramitos)-1].origen
				tramo2.destino = par2
				tramo2.distancia = 0
				tramo2.viaje = viaje.id
				tramo2.save()
				pks[len(tramitos)-1] = tramo2.id
				i=1
				while(i<len(tramitos)-1):
					tramitos[i].asientos_disponibles = form.cleaned_data['asientos_disponibles'] 
					tramitos[i].save()
					i=i+1
				viaje.tramos.clear()
				i = 0
				for pk in pks:
					tramon = Tramo.objects.get(id = pk)
					tramon.asientos_disponibles = form.cleaned_data['asientos_disponibles'] 
					viaje.tramos.add(tramon)
					i +=1
				viaje.porta_maleta=form.cleaned_data['porta_maleta']
				viaje.silla_niños=form.cleaned_data['silla_niños']
				viaje.mascotas=form.cleaned_data['mascotas']
				viaje.tarifaPreferencias=form.cleaned_data['tarifapreferencias']
				viaje.plazas_disponibles=form.cleaned_data['asientos_disponibles'] 
				viaje.fecha = form.cleaned_data['fecha']
				print(form.cleaned_data['fecha'])
				viaje.save()
			
			if request.POST.get("publicar4"):
				#request.session['viaje']['paradas'] = aux
				return Editarlisto(request,idviaje)
		else:
			data= {'fecha':viaje.fecha, 
				'porta_maleta':viaje.porta_maleta,
				'silla_niños':viaje.silla_niños,
				'mascotas':viaje.mascotas ,
				'tarifapreferencias':viaje.tarifaPreferencias,
				'asientos_disponibles':viaje.plazas_disponibles,
				'hora_origen':tramitos[0].hora_salida, 
				'fecha_destino':tramitos[len(tramitos)-1].fecha, 
				'hora_destino':tramitos[len(tramitos)-1].hora_llegada,
				'destino':tramitos[len(tramitos)-1].destino.nombre,
				'origen':tramitos[0].origen.nombre}
			form = EditarViajeForm(initial=data)
			return render(request, 'viaje/editarviaje.html', {'form':form})
	#return render(request, 'viaje/editarviaje.html', {'form':form})		

@login_required()
def Editarlisto(request,idviaje):
	viaje = Viaje.objects.get(id=idviaje)
	tramitos = viaje.tramos.all()
	paradas = []
	pks = []
	for t in tramitos:
		pks.append(t.id)
	i=0
	while(i < len(tramitos)):
		if(i== len(tramitos)-1):
			paradas.append(tramitos[i].origen.direccion)	
			paradas.append(tramitos[i].destino.direccion)	
		else:	
			paradas.append(tramitos[i].origen.direccion)
		i=i+1	
	if request.method == "POST":
		if request.POST.get("listo"):
			distancias = request.POST['holiwi'].split()
			aux = []
			for i in range(len(distancias)//2):
				aux.append(float(distancias[2*i].replace(',','')))

			tramo1 = Tramo()
			tramo1.orden_en_viaje  = 0
			tramo1.hora_salida = tramitos[0].hora_salida
			tramo1.hora_llegada = tramitos[0].hora_llegada
			tramo1.fecha = tramitos[0].fecha
			tramo1.asientos_disponibles = tramitos[0].asientos_disponibles
			tramo1.origen = tramitos[0].origen
			tramo1.destino = tramitos[0].destino
			tramo1.distancia = aux[0]
			tramo1.viaje = viaje.id
			tramo1.save()
			pks[0] = tramo1.id

			tramo2 = Tramo()
			tramo2.orden_en_viaje  = len(tramitos)-1
			tramo2.hora_salida = tramitos[len(tramitos)-1].hora_salida
			tramo2.hora_llegada = tramitos[len(tramitos)-1].hora_llegada
			tramo2.fecha =  tramitos[len(tramitos)-1].fecha
			tramo2.asientos_disponibles = tramitos[len(tramitos)-1].asientos_disponibles
			tramo2.origen = tramitos[len(tramitos)-1].origen
			tramo2.destino = tramitos[len(tramitos)-1].destino
			tramo2.distancia = aux[len(tramitos)-1]
			tramo2.viaje = viaje.id
			tramo2.save()
			pks[len(tramitos)-1] = tramo2.id
			viaje.tramos.clear()
			i = 0
			for pk in pks:
				tramon = Tramo.objects.get(id = pk)
				viaje.tramos.add(tramon)
				i +=1
			viaje.save()	
			return redirect('index')
		elif request.POST.get("publicar4"):
			json_cities = json.dumps(paradas)
			return render (request, 'viaje/editarlisto.html', {"city_array" : json_cities, "paradas": paradas, "max": len(paradas)-1})
	else:
		raise Http404  

@login_required()
def confirmarCan(request, pk):
	if(tiene_reservas(pk)):
		return redirect('cancelar_editar_error')
	return render(request, 'viaje/confirmarCanc.html', {'id' : pk})

@login_required()
def cancelar(request, pk):
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
		tramitos=viaje.tramos.all().order_by('orden_en_viaje')
		asientos=viaje.plazas_disponibles
		for tr in tramitos:
			if aux:
				tramos.append([tr,viaje.plazas_disponibles-tr.asientos_disponibles])
				distancia+=tr.distancia
				if tr.asientos_disponibles<asientos:
					asientos=tr.asientos_disponibles
			if tr.origen.nombre == Origen and aux==False:
				tramos.append([tr,viaje.plazas_disponibles-tr.asientos_disponibles])
				distancia+=tr.distancia
				asientos=tr.asientos_disponibles
				aux=True
			if aux and tr.destino.nombre == Destino:
				ultimo=tr
				if tr.asientos_disponibles<asientos:
					asientos=tr.asientos_disponibles
				break
		precio=distancia*viaje.tarifaPreferencias
		v=[idviaje,precio,distancia,asientos]
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
				print(tram.asientos_disponibles)
				reserva.tramos.add(tram)	
				aux=True

			if tram.origen.nombre == origen and aux==False:
				reserva.tramos.add(tram)	
				aux=True		
			
			if tram.destino.nombre == destino:
				break
		reserva.save()

		tremos = reserva.tramos.all()
		if v.conductor.autoaceptar_reservas:#Aceptar automaticamente
			print("Autoaceptando")
			aceptarreserva = True
			for tram in tremos:#revisar disponibilidad de cada tramo
				if int(asientos) > tram.asientos_disponibles:
					aceptarreserva = False
					print("No autoaceptado")
					break
			if aceptarreserva:
				for tram in tremos:
					tram.asientos_disponibles -= int(asientos)
					tram.save()
				reserva.estado="Aprobada"
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
	r=Reserva.objects.get(id=pk)
	if(request.POST.get("encurso") is not None):
		idv = r.tramos.all()[0].viaje
		return render(request, 'viaje/confirmarCanReservaConductor.html', {'id' : pk , 'id2' : idv})
	else:
		print('E')

	return render(request, 'viaje/confirmarCanReservaConductor.html', {'id' : pk})

@login_required()
def cancelarReservaConductor(request, pk):
	reservas = Reserva.objects.filter(id=pk)
	reserva = reservas[0]
	u = Usuario.objects.get(id=request.user.pk)
	conductor = u.conductor_set.all()[0]
	if(reserva.estado == "Por Aprobar"):
		reserva.estado = "Rechazada"
		conductor.reservas_por_aprobar -= 1
		conductor.save()
		reserva.save()
		exitocancelarreservaconductor = True
	#	return render(request, 'viaje/cancelarReservaConductor.html', {'exitocancelarreservaconductor' : exitocancelarreservaconductor})
	else:
		exitocancelarreservaconductor = False
	#	return render(request, 'viaje/cancelarReservaConductor.html', {'exitocancelarreservaconductor' : exitocancelarreservaconductor})
	if(request.POST.get("encurso") is not None):
		encurso = True
		idv = reserva.tramos.all()[0].viaje
		return render(request, 'viaje/cancelarReservaConductor.html', {'exitocancelarreservaconductor' : exitocancelarreservaconductor , 'encurso' : encurso, 'id2' : idv})
	else:
		encurso = False

	return render(request, 'viaje/cancelarReservaConductor.html', {'exitocancelarreservaconductor' : exitocancelarreservaconductor , 'encurso' : encurso})

@login_required()
def confirmarCanReservaAceptadaConductor(request, pk):
	return render(request, 'viaje/confirmarCanReservaAceptadaConductor.html', {'id' : pk})

@login_required()
def cancelarReservaAceptadaConductor(request, pk):
	reservas = Reserva.objects.filter(id=pk)
	reserva = reservas[0]
	u = Usuario.objects.get(id=request.user.pk)
	conductor = u.conductor_set.all()[0]
	tramosreserva = reserva.tramos.all()
	for t in tramosreserva:
		for i in tramosreserva:
			i.asientos_disponibles += reserva.plazas_pedidas
			i.save()
		reserva.estado = "Por Aprobar"
		conductor.reservas_por_aprobar += 1
		conductor.save()
		reserva.save()
		exitocancelarreservaaceptadaconductor = True
		return render(request, 'viaje/cancelarReservaAceptadaConductor.html', {'exitocancelarreservaaceptadaconductor' : exitocancelarreservaaceptadaconductor})
	else:
		exitocancelarreservaaceptadaconductor = False
		return render(request, 'viaje/cancelarReservaAceptadaConductor.html', {'exitocancelarreservaaceptadaconductor' : exitocancelarreservaaceptadaconductor})

@login_required()
def confirmarAceptarReservaConductor(request, pk):
	r=Reserva.objects.get(id=pk)
	if(request.POST.get("encurso") is not None):
		print('viaje en curso')
		#dire = 'administrar'
		idv = r.tramos.all()[0].viaje
		return render(request, 'viaje/confirmarAceptarReservaConductor.html', {'id' : pk , 'id2' : idv})#, 'rechazo' : dire})
	else:
		print('E')
		#dire = 'viaje_list'

	return render(request, 'viaje/confirmarAceptarReservaConductor.html', {'id' : pk })#, 'rechazo' : dire})

@login_required()
def aceptarReservaConductor(request, pk):
	reservas = Reserva.objects.filter(id=pk)
	reserva = reservas[0]
	u = Usuario.objects.get(id=request.user.pk)
	conductor = u.conductor_set.all()[0]
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
			i.asientos_disponibles -= reserva.plazas_pedidas
			i.save()
		reserva.estado = "Aprobada"
		conductor.reservas_por_aprobar -= 1
		conductor.save()
		reserva.save()
		exitoaceptarreservaconductor = True
	#	return render(request, 'viaje/aceptarReservaConductor.html', {'exitoaceptarreservaconductor' : exitoaceptarreservaconductor})
	else:
		exitoaceptarreservaconductor = False
	#	return render(request, 'viaje/aceptarReservaConductor.html', {'exitoaceptarreservaconductor' : exitoaceptarreservaconductor})

	if(request.POST.get("encurso") is not None):
		encurso = True
		idv = reserva.tramos.all()[0].viaje
		return render(request, 'viaje/aceptarReservaConductor.html', {'exitoaceptarreservaconductor' : exitoaceptarreservaconductor , 'encurso' : encurso, 'id2' : idv})
	else:
		encurso = False

	return render(request, 'viaje/aceptarReservaConductor.html', {'exitoaceptarreservaconductor' : exitoaceptarreservaconductor})

def administrar(request,pk):
	try:
		viaje = Viaje.objects.get(id=pk)
	except:
		raise Http404
	if viaje.conductor.usuario == request.user and viaje.estado == "Iniciado":
		reservas = []
		reservasaceptadas = []
		reservastransito = []
		r=Reserva.objects.all()
		
		for reserva in r:
			if (reserva.estado == "Por Aprobar"):
				tramosreserva = reserva.tramos.all()
				aux = []
				if reserva.tramos.all()[0].viaje == int(pk):
					aux.append(reserva.id)
					aux.append(reserva.plazas_pedidas)
					aux.append(tramosreserva[0].origen.nombre)
					aux.append(tramosreserva[len(tramosreserva)-1].destino.nombre)
					aux.append(reserva.precio)
					aux.append(reserva.estado)
					aux.append(reserva.usuario)
					reservas.append(aux)
			if (reserva.estado == "Transito"):
				tramosreserva = reserva.tramos.all()
				aux = []
				if reserva.tramos.all()[0].viaje == int(pk):
					aux.append(reserva.id)
					aux.append(reserva.plazas_pedidas)
					aux.append(tramosreserva[0].origen.nombre)
					aux.append(tramosreserva[len(tramosreserva)-1].destino.nombre)
					aux.append(reserva.precio)
					aux.append(reserva.estado)
					aux.append(reserva.usuario)
					reservastransito.append(aux)
		tramo_especial = viaje.tramos.all().filter(orden_en_viaje = viaje.parada_actual-1)[0]
		print(tramo_especial.origen.direccion)
		reservas_especiales = tramo_especial.reservas.all()
		print(reservas_especiales)
		for res in reservas_especiales:
			if res.estado == "Aprobada":
				tramosreserva = reserva.tramos.all()
				aux = []				
				aux.append(reserva.id)
				aux.append(reserva.plazas_pedidas)
				aux.append(tramosreserva[0].origen.nombre)
				aux.append(tramosreserva[len(tramosreserva)-1].destino.nombre)
				aux.append(reserva.precio)
				aux.append(reserva.estado)
				aux.append(reserva.usuario)
				reservasaceptadas.append(aux)
		tramitos = viaje.tramos.all().order_by('orden_en_viaje')
		paradas = []						
		for i in range(len(tramitos)):
			paradas.append(tramitos[i].origen.direccion)
		paradas.append(tramitos[len(tramitos)-1].destino.direccion)

		if request.method == "GET":
			print(viaje.parada_actual)
			if viaje.parada_actual == len(tramitos)+1:
					viaje.estado = "Terminado"
					viaje.save()
					request.session['valoraciones'] = viaje.id
					return redirect('home') 
			json_cities = json.dumps(paradas[viaje.parada_actual-1::])
			destino = False
			if(viaje.parada_actual < len(tramitos)-1):
				sig = tramitos[viaje.parada_actual]
			else:
				sig = tramitos[viaje.parada_actual-1]
				destino = True
			return render (request, 'conductor/administrar.html', {"city_array" : json_cities, "siguiente": sig, "destino": destino,'reservas':reservas,'reservastransito':reservastransito,'reservasaceptadas':reservasaceptadas})

		elif request.method == 'POST':
			if request.POST.get("parada"):
				viaje.parada_actual+=1
				viaje.save()
			if viaje.parada_actual == len(tramitos)+1:
				viaje.estado = "Terminado"
				viaje.save()
				request.session['valoraciones'] = viaje.id
				return redirect('home') # esto debe cambiarse
			json_cities = json.dumps(paradas[viaje.parada_actual-1::])
			destino = False
			if(viaje.parada_actual < len(tramitos)-1):
				sig = tramitos[viaje.parada_actual]
			else:
				sig = tramitos[viaje.parada_actual-1]
				destino = True
			if request.POST.get("parada"):
				return render (request, 'conductor/administrar.html', {"city_array" : json_cities, "siguiente": sig, "destino": destino,'reservas':reservas,'reservastransito':reservastransito,'reservasaceptadas':reservasaceptadas})
			
			elif request.POST.get("baja"):
				print("boton_baja")
				id_res = request.POST.get("baja")
				reservas = Reserva.objects.filter(id=id_res)
				reserva = reservas[0]
				if(reserva.estado == "Transito"):
					reserva.estado = "Terminada"
					reserva.save()
				return render (request,'conductor/administrar.html', {"city_array" : json_cities, "siguiente": sig, "destino": destino,'reservas':reservas,'reservastransito':reservastransito,'reservasaceptadas':reservasaceptadas})
			
			elif request.POST.get("sube"):		
				print("boton_subee")
				print(request.POST.get("sube"))
				id_res = request.POST.get("sube")
				reservas = Reserva.objects.filter(id=id_res)
				if(reserva.estado == "Aprobada"):
					reserva.estado = "Transito"
					reserva.save()
					print(reserva.estado)
				return render(request,'conductor/administrar.html', {"city_array" : json_cities, "siguiente": sig, "destino": destino,'reservas':reservas,'reservastransito':reservastransito,'reservasaceptadas':reservasaceptadas})
		
			elif request.POST.get("nosube"):
				print("boton no sube", request.POST.get("no sube"))
				pks = request.POST.get("nosube")
				reservas = Reserva.objects.filter(id=pks)
				reserva = reservas[0]
				tramosreserva = reserva.tramos.all()
				for t in tramosreserva:
					for i in tramosreserva:
						i.asientos_disponibles += reserva.plazas_pedidas
						i.save()
					viaje.asientos_disponibles +=reserva.plazas_pedidas
					viaje.save() 
					reserva.estado = "Abortada"
					reserva.save()
				return render(request, 'conductor/administrar.html', {"city_array" : json_cities, "siguiente": sig, "destino": destino,'reservas':reservas,'reservastransito':reservastransito,'reservasaceptadas':reservasaceptadas})	

			elif request.POST.get("alerta"):		
				if(destino):
					mandar_alerta(pk,tramitos[viaje.parada_actual-1].destino.id)
				else:
					mandar_alerta(pk,tramitos[viaje.parada_actual-1].origen.id)	
				return render(request,'conductor/administrar.html', {"city_array" : json_cities, "siguiente": sig, "destino": destino,'reservas':reservas,'reservastransito':reservastransito,'reservasaceptadas':reservasaceptadas})

			elif request.POST.get("aprobar"):		
				print(request.POST.get("aprobar"))
				return render(request,'conductor/administrar.html', {"city_array" : json_cities, "siguiente": sig, "destino": destino,'reservas':reservas,'reservastransito':reservastransito,'reservasaceptadas':reservasaceptadas})

	
		else:
			raise Http404
	else:
		raise Http404

def detail_viaje_en_curso(request,pk):
	try:
		r = Reserva.objects.get(id=pk)
		v = Viaje.objects.get(id = r.tramos.all()[0].viaje)
		if(r.usuario == request.user and v.estado == "Iniciado" and (r.estado == "Aprobada" or r.estado == "Transito")):
			tramos = v.tramos.all().order_by('orden_en_viaje')
			jotason = []
			for i in range(len(tramos)):
				jotason.append(tramos[i].origen.direccion)
				if(i == len(tramos)-1):
					jotason.append(tramos[i].destino.direccion)
			json_cities = json.dumps(jotason)
			if (v.parada_actual-1 == len(tramos)+1):
				actual = tramos[len(tramos)-1].destino.direccion
			else:
				actual = tramos[v.parada_actual-1].origen.direccion
			actual = json.dumps(actual)
			return render (request, 'viaje/viaje_reserva.html', {"city_array" : json_cities, "paradas": jotason[v.parada_actual-1::], "nombre": jotason[v.parada_actual-1], "actual": actual})
		else:
			raise Http404
	except:
		raise Http404


def mandar_alerta(id_viaje,parada):
	v = Viaje.objects.filter(id=id_viaje)[0]
	tramos = v.tramos.all().order_by('orden_en_viaje')
	for tramo in tramos:
		if(tramo.origen.id) == parada:
			for reserva in tramo.reservas.all():
				if (reserva.estado == "Aprobada"):
					reserva.usuario.perfil.mensajes = "El conductor esta cerca del punto de encuentro"
					reserva.usuario.perfil.save()
					break
	return 0

def iniciarviaje(request,pk):
	v = Viaje.objects.filter(id=pk)[0]
	tz = pytz.timezone('Chile/Continental')
	actual = datetime.strptime(datetime.now(tz=tz).strftime("%d/%m/%Y %H:%M:%S") , "%d/%m/%Y %H:%M:%S")
	fecha_origen = datetime.strptime(datetime.combine(v.fecha,v.tramos.all()[0].hora_salida).strftime("%d/%m/%Y %H:%M:%S") , "%d/%m/%Y %H:%M:%S")
	if(v.estado == "Iniciado"):
		return redirect('administrar',pk=pk)
	if(v.conductor.usuario == request.user and v.estado=="Registrado" and abs(actual - fecha_origen) < timedelta(minutes=30)):
		mandar_alerta(pk,v.tramos.all()[0].origen.id)
		v.estado = "Iniciado"
		v.save()
		return redirect('administrar',pk=pk)
	titulo = "No se puede inicar viaje"
	mensaje = "El viaje no cumple con las condiciones para ser iniciado."
	return render(request,'conductor/error.html',{"titulo" : titulo, "mensaje" : mensaje})
#@login_required()
#def Viajereservasver(request):		
