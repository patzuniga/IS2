from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse

from apps.viaje.forms import ParadasForm, ViajeForm, BuscarForm
from apps.viaje.models import Viaje, Tramo, Parada
from apps.conductor.models import Conductor
from apps.usuario.models import Usuario
from django.views.generic import ListView
from django.forms import formset_factory

def index(request):
	return render(request,'viaje/index.html')

def viaje_view(request):
	if request.method == 'POST':
		form = ViajeForm(request.POST)
		if form.is_valid():
			viaje = Viaje()
			viaje.fecha = form.cleaned_data['fecha']
			viaje.estado = "Registrado"
			viaje.porta_maleta = form.cleaned_data['porta_maleta']
			viaje.mascotas = form.cleaned_data['mascotas']
			viaje.tarifapreferencias = form.cleaned_data['tarifapreferencias']
			viaje.max_personas_atras = form.cleaned_data['max_personas_atras']
			current_user = request.user
			u = Usuario.objects.get(id=current_user.id)
			viaje.conductor = u.conductor_set.all()[0]
			viaje.save()
			aux = []
			request.session['viaje'] = viaje.id
			print(request.session['viaje'])
			#Paradas en aux
			aux.append([form.cleaned_data['fecha'].strftime("%d/%m/%Y"), form.cleaned_data['hora_origen'], form.cleaned_data['origen'].split()[0], form.cleaned_data['origen']])
			aux.append([form.cleaned_data['fecha_destino'].strftime("%d/%m/%Y"), form.cleaned_data['hora_destino'], form.cleaned_data['destino'].split()[0], form.cleaned_data['destino']])
			request.session['paradas'] = aux
			return redirect('paradas')
		else:
			return render(request,'viaje/paradas.html',{'form':form})
	else:
		form = ViajeForm()
		return render(request,'viaje/crear2.html',{'form':form})

def viaje_list(request):
	viaje = Viaje.objects.all()
	contexto = {'viajes':viaje}
	return render(request, 'viaje/viaje_list.html', contexto)

def viaje_listo(request):
	viaje  = Viaje.objects.get(id = Viaje.objects.latest('id').id)
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
	return viaje_ver(request)

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
			lista.append(aux)
	return render(request, 'viaje/viaje_list.html', {'viajes':lista})

def success(request):
	return render(request, 'viaje/listo.html', {})	

def viaje_paradas(request):
	if request.method == 'GET':
		try:
			viaje = request.session['viaje']
			form = ParadasForm()
			return render(request,'viaje/paradas.html',{'form':form})
		except:
			form = ParadasForm()
			return render(request,'viaje/paradas.html',{'form':form})
	else:
		aux = []
		aux = request.session['paradas']
		form = ParadasForm(request.POST)
		if request.POST.get("agregar"):
			if form.is_valid():
				direccion = str(request.POST['direccion'])
				aux.append([form.cleaned_data['fecha'].strftime("%d/%m/%Y"), form.cleaned_data['hora'],direccion.split(',')[0], direccion])
				request.session['paradas'] = aux
				form = ParadasForm()
				return render(request,'viaje/paradas.html',{'form':form})
			else:
				form = ParadasForm()
				return render(request,'viaje/paradas.html',{'form':form})
		elif request.POST.get("publicar"):
			if form.is_valid():
				direccion = str(request.POST['direccion'])
				aux.append([form.cleaned_data['fecha'].strftime("%d/%m/%Y"), form.cleaned_data['hora'],direccion.split(',')[0], direccion])
				request.session['paradas'] = aux
				return viaje_listo(request)
			else:
				return viaje_listo(request)

import json

def viaje_ver(request):
<<<<<<< HEAD
	if request.method == "POST":
		aux = request.POST['holiwi'].split()
		print(aux)
		viaje  = Viaje.objects.get(id = Viaje.objects.latest('id').id)
		tramitos = viaje.tramos.all()
		if(len(aux)//2 == len(tramitos)):
			for i in range(len(tramitos)):
				tramitos[i].distancia = float(aux[2*i])
				tramitos[i].save()
			return render(request, 'viaje/listo.html', {})	
		else:
			return render(request, 'viaje/listo.html', {})
	else:
		paradas = []
		print("viaje get :",Viaje.objects.latest('id'))
		print("viaje id : ", Viaje.objects.latest('id').id)
		viaje  = Viaje.objects.get(id = Viaje.objects.latest('id').id)
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

def buscar_viaje(request):
	if request.method == "GET":
		return render(request, 'viaje/buscar.html', {})
	else:
		resultado = []
		form = BuscarForm(request.POST)
		f = form.cleaned_data['fecha'].strftime("%d/%m/%Y")
		s = form.cleaned_data['origen'].split()[0]
		t = form.cleaned_data['destino'].split()[0]
		viaje  = Viaje.objects.all()
		#se revisan todos lo viajes
		for v in viaje:
			origen = False
			destino = False
			distancia = 0;
			tramitos = viaje.tramos.all()
			#se revisan los tramos del viaje
			for t in tramitos:
				#Como el origen se debe encontrar primero y no sirve que la ultima parada del viaje coincida con este, solo se revisa la primera parada del tramo
				if(t.origen.nombre == s):
					distancia = 0;
					origen = True
				#Solo importa ver si el destino existe cuando ya se encontró el origen
				if(origen):
					distancia += t.distancia
					#si es que los asientos disponibles son 0 en el camino, el viaje no sirve. Pero debo seguir revisando ya que se podria pasar por ahi de nuevo
					# y alli podrian haber asientos disponibles
					if(t.asientos_disponibles == 0):
						origen = False
					elif(t.destino.nombre == t):
						destino = True
						break
			if(origen and destino):
				resultado.append([v,distancia])
		if(resultado):
			size = len(resultado)
			return render(request, 'viaje/buscar2.html', {'viajes':resultado, 'size':size, 'origen':s, 'destino':t})


				 
=======
	paradas = []
	viaje  = Viaje.objects.get(id = Viaje.objects.latest('id').id)
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
	print(ultimo)
	return render (request,'viaje/ejemplo.html', {'paradas':json_cities, 'ultimo':ultimo})

def buscar_viaje(request):
	if request.method == 'POST':
		form = BuscarForm(request.POST)

	else:
		form = BuscarForm()
	return render(request,'viaje/buscarviaje.html',{'form':form})	
>>>>>>> ab1f588858fa7d9a5ac7523d7d1fe9d502eb8513
