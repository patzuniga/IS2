from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse

from apps.viaje.forms import ParadasForm, ViajeForm
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
	aux.sort()
	for i in range(0,len(aux),2):
		par1 = Parada()
		par1.nombre = aux[i][2]
		par1.direccion = aux[i][3]
		par1.save()

		par2 = Parada()
		par2.nombre = aux[i+1][2]
		par2.direccion = aux[i+1][3]
		par2.save()

		tramo = Tramo()
		tramo.orden_en_viaje  = i
		tramo.hora_salida = aux[i][1]
		tramo.hora_llegada = aux[i+1][1]
		tramo.fecha = aux[i][0]
		tramo.asientos_disponibles = viaje.max_personas_atras + 1
		tramo.origen = par1
		tramo.destino = par2
		tramo.save()

		viaje.tramos.add(tramo)
	aux = []
	viaje.save()
	return redirect("viaje/success")

def Viajelist(request):
	lista = []
	for v in Viaje.objects.all():
		if v.conductor == request.user._conductor:
			tramito = v.tramos.all()
			lista.append(tramito[0])
	return render(request, 'viaje/viaje_list.html', {'viajes':lista})

def success(request):
	return render(request, 'viaje/listo.html', {})	
#Pasarle direccion y ciudad (inlcuirlo en el html de paradas)
#ver si aux esta vacío y ahi mandar la pag
#actulizar paradas 
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
		if form.is_valid():
			direccion = str(request.POST['direccion'])
			aux.append([form.cleaned_data['fecha'].strftime("%d/%m/%Y"), form.cleaned_data['hora'],direccion.split(',')[0], direccion])
			request.session['paradas'] = aux
			form = ParadasForm()
			return render(request,'viaje/paradas.html',{'form':form})
		else:
			form = ParadasForm()
			return render(request,'viaje/paradas.html',{'form':form})

import json

def viaje(request):
	paradas = []
	viaje = Viaje.objects.get(id=13)
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
