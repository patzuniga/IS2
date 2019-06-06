from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse

from apps.viaje.forms import ParadasForm, ViajeForm, BuscarForm
from apps.viaje.models import Viaje, Tramo, Parada
from apps.conductor.models import Conductor
from apps.usuario.models import Usuario
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory

def index(request):
	return render(request,'viaje/index.html')

@login_required()
def viaje_view(request):
	if request.method == 'POST':
		form = ViajeForm(request.POST)
		if form.is_valid():
			viaje = Viaje()
			viaje.fecha = form.cleaned_data['fecha']
			viaje.estado = "Registrado"
			viaje.porta_maleta = form.cleaned_data['porta_maleta']
			viaje.mascotas = form.cleaned_data['mascotas']
			viaje.tarifaPreferencias = form.cleaned_data['tarifapreferencias']
			viaje.max_personas_atras = form.cleaned_data['max_personas_atras']
			current_user = request.user
			u = Usuario.objects.get(id=current_user.id)
			viaje.conductor = u.conductor_set.all()[0]
			viaje.save()
			aux = []
			request.session['viaje'] = viaje.id
			print(request.session['viaje'])
			#Paradas en aux
			aux.append([form.cleaned_data['fecha'].strftime("%d/%m/%Y"), form.cleaned_data['hora_origen'].strftime("%H:%M"), form.cleaned_data['origen'].split()[0], form.cleaned_data['origen']])
			aux.append([form.cleaned_data['fecha_destino'].strftime("%d/%m/%Y"), form.cleaned_data['hora_destino'].strftime("%H:%M"), form.cleaned_data['destino'].split()[0], form.cleaned_data['destino']])
			request.session['paradas'] = aux
			return redirect('paradas', pk = viaje.id)
		else:
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
def viaje_listo(request, pk):
	viaje  = Viaje.objects.get(id = pk)
	aux = request.session['paradas']
	aux.sort()
	for i in range(0,len(aux)-1):
		if(i==0):
			par1 = Parada()
			par1.nombre = aux[i][2]
			par1.direccion = aux[i][3]
			par1.save()

			par2 = Parada()
			par2.nombre = aux[i+1][2]
			par2.direccion = aux[i+1][3]
			par2.save()
		else:
			par1 = par2
			par2 = Parada()
			par2.nombre = aux[i+1][2]
			par2.direccion = aux[i+1][3]
			par2.save()

		tramo = Tramo()
		tramo.orden_en_viaje  = i
		tramo.hora_salida = aux[i][1]
		tramo.hora_llegada = aux[i+1][1]
		tramo.fecha = aux[i][0]
		tramo.asientos_disponibles = viaje.max_personas_atras
		tramo.origen = par1
		tramo.destino = par2
		tramo.save()

		viaje.tramos.add(tramo)
	aux = []
	viaje.save()
	return redirect("mapa_ejemplo", pk)

@login_required()
def Viajelist(request):
	lista = []
	current_user = request.user
	u = Usuario.objects.get(id=current_user.id)
	conductor = u.conductor_set.all()[0]
	for v in Viaje.objects.all():
		if v.conductor == conductor:
			aux = []
			tramito = v.tramos.all()
			aux.append(v)
			aux.append(tramito[0])
			aux.append(tramito[len(tramito)-1])
			aux.append(str(v.fecha).split()[0])
			lista.append(aux)
	return render(request, 'viaje/viaje_list.html', {'viajes':lista})

@login_required()
def success(request, pk):
	viaje  = Viaje.objects.get(id = pk)
	return render(request, 'viaje/listo.html', {'id': pk})	

#Funcion que se conecta con agregar paradas, se llama asi misma hasta que se publique el viaje o se aprete cancelar
@login_required()
def viaje_paradas(request,pk):
	if request.method == 'GET':
		form = ParadasForm()
		return render(request,'viaje/paradas.html',{'form':form})
	else:
		aux = []
		aux = request.session['paradas']
		form = ParadasForm(request.POST)
		if form.is_valid():
			print(type(aux[1][0]))
			print(type(aux[1][0]))
			viaje = Viaje.objects.get(id = pk)
			fo = viaje.fecha.strftime("%d/%m/%Y")
			fd = aux[1][0]
			fp = form.cleaned_data['fecha'].strftime("%d/%m/%Y")
			ho = aux[0][1]
			hd =  aux[1][1]
			hp = form.cleaned_data['hora'].strftime("%H:%M")
			print("hora ",hp)
			print("hora origen ",ho)
			print("hora destino ",hd)
			print(hp > hd, "hora parada mayor que hora destino")
			if (fp < fo or fd < fp or (fo == fp and hp <= ho) or (fd == fp and hd <= hp)):
				error = "Fecha y hora de la parada deben ser consistentes con las fechas y horas de origen y destino."
				form = ParadasForm()
				return render(request,'viaje/paradas.html',{'form':form, 'error': error})
			elif request.POST.get("agregar"):
				direccion = str(request.POST['direccion'])
				aux.append([fp, hp,direccion, direccion.split(',')[0]])
				request.session['paradas'] = aux
				form = ParadasForm()
				return render(request,'viaje/paradas.html',{'form':form})
			elif request.POST.get("publicar"):
					direccion = str(request.POST['direccion'])
					aux.append([fp, hp,direccion, direccion.split(',')[0]])
					request.session['paradas'] = aux
					return viaje_listo(request, pk)
			else:
				error = "Ha ocurrido un error inesperado. Disculpe por las molestias"
				form = ParadasForm()
				return render(request,'viaje/paradas.html',{'form':form, 'error': error})
		elif request.POST.get("publicar"):
			request.session['paradas'] = aux
			return viaje_listo(request, pk)
		else:
			form = ParadasForm()
			return render(request,'viaje/paradas.html',{'form':form})

import json

#Funcion que se encarga de pasarle todos las paradas del viaje al mapa para mostrar el viaje
@login_required()
def viaje_ver(request, pk):
	if request.method == "POST":
		aux = request.POST['holiwi'].split()
		print(aux)
		viaje  = Viaje.objects.get(id = pk)
		tramitos = viaje.tramos.all()
		if(len(aux)//2 == len(tramitos)):
			for i in range(len(tramitos)):
				tramitos[i].distancia = float(aux[2*i])
				tramitos[i].save()
			return success(request,pk)	
		else:
			return success(request,pk)
	else:
		paradas = []
		viaje  = Viaje.objects.get(id = pk)
		print(viaje)
		tramitos = viaje.tramos.all()
		ultimo = len(tramitos)
		for i in range(len(tramitos)):
			if i != len(tramitos)-1:
				paradas.append(tramitos[i].origen.direccion)
			else :
				paradas.append(tramitos[i].origen.direccion)
				paradas.append(tramitos[i].destino.direccion)
		print(paradas)
		json_cities = json.dumps(paradas)
		print(json_cities)
		return render (request, 'viaje/ejemplo.html', {"city_array" : json_cities})

@login_required()
def buscar_viaje(request):
	if request.method == 'GET':
		form = BuscarForm()
		return render(request,'viaje/buscarviaje.html',{'form':form})
	else:
		resultado = []
		form = BuscarForm(request.POST)
		if form.is_valid():
			f = form.cleaned_data['fecha']
			s = form.cleaned_data['origen'].split()[0]
			u = form.cleaned_data['destino'].split()[0]
			viaje  = Viaje.objects.all()
			#se revisan todos lo viajes
			for v in viaje:
				origen = False
				destino = False
				distancia = 0;
				tramitos = v.tramos.all()
				print(tramitos)
				print(v.tarifaPreferencias)
				#se revisan los tramos del viaje
				for t in tramitos:
					print(t)
					print(t.distancia)
					print(origen)
					print(t.origen.nombre , s)
					print(t.destino.nombre, u)
					#Como el origen se debe encontrar primero y no sirve que la ultima parada del viaje coincida con este, solo se revisa la primera parada del tramo
					if(t.origen.nombre == s):
						distancia = 0;
						origen = True
						print(origen)
					#Solo importa ver si el destino existe cuando ya se encontró el origen
					if(origen):
						distancia += float(t.distancia)
						#si es que los asientos disponibles son 0 en el camino, el viaje no sirve. Pero debo seguir revisando ya que se podria pasar por ahi de nuevo
						# y alli podrian haber asientos disponibles
						if(t.asientos_disponibles == 0):
							origen = False
						elif(t.destino.nombre == u):
							destino = True
							break
				if(origen and destino):
					resultado.append([v,tramitos[0], tramitos[len(tramitos)-1],distancia*v.tarifaPreferencias])
			return render(request, 'viaje/buscar2.html', {'viajes':resultado, 'origen':s, 'destino':u})
		else:
			return render(request,'viaje/buscarviaje.html',{'form':form})

def tiene_reservas(pk):
	aux = Viaje.objects.get(id = pk)
	tramitos = aux.tramos.all()
	for i in tramitos:
		try:
			aux = tramitos.reserva
			return True
		except:
			continue
	return False

@login_required()
def viaje_details(request, pk):
	viajes=[]
	if request.method == 'GET':
		aux = Viaje.objects.get(id = pk)
		tramitos = aux.tramos.all()
		viajes.append(aux)
		viajes.append(tramitos)
		viajes.append(str(aux.fecha).split()[0])

	paradas = []
	viaje  = Viaje.objects.get(id = pk)
	tramitos = viaje.tramos.all()
	ultimo = len(tramitos)
	for i in range(len(tramitos)):
		if i != len(tramitos)-1:
			paradas.append(tramitos[i].origen.direccion)
		else :
			paradas.append(tramitos[i].origen.direccion)
			paradas.append(tramitos[i].destino.direccion)
	json_cities = json.dumps(paradas)
	return render(request, 'viaje/viaje_details.html', {'viajes':viajes, 'paradas':json_cities, 'ultimo':ultimo})


@login_required()
def editarviaje(request):
	if request.method == 'GET':
		lol = request.GET["idviaje"]
		viaje = Viaje.objects.get(id = lol)
	return render (request, "viaje/editarviaje.html", {"viaje": viaje})
