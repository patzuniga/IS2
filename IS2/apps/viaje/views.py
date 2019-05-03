from django.shortcuts import render, redirect
from django.http import HttpResponse

from apps.viaje.forms import ViajeForm
from apps.viaje.models import Viaje, Tramo, Parada
from apps.conductor.models import Conductor
from apps.usuario.models import Usuario
from django.views.generic import ListView

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
			viaje.conductor = request.user._conductor
			viaje.save()

			par1 = Parada()
			par1.nombre = form.cleaned_data['origen'].split()[0]
			par1.direccion = form.cleaned_data['origen']
			par1.save()

			par2 = Parada()
			par2.nombre = form.cleaned_data['destino'].split()[0]
			par2.direccion = form.cleaned_data['destino']
			par2.save()

			tramo = Tramo()
			tramo.orden_en_viaje  = 1
			tramo.hora_salida = form.cleaned_data['hora_origen']
			tramo.hora_llegada = form.cleaned_data['hora_destino']
			tramo.fecha = form.cleaned_data['fecha']
			tramo.asientos_disponibles = form.cleaned_data['max_personas_atras'] + 1
			tramo.origen = par1
			tramo.destino = par2
			tramo.save()

			viaje.tramos.add(tramo)
			viaje.save()
			return redirect('viaje_listo')
	else:
		form = ViajeForm()
	return render(request,'viaje/crear.html',{'form':form})

def viaje_list(request):
	viaje = Viaje.objects.all()
	contexto = {'viajes':viaje}
	return render(request, 'viaje/viaje_list.html', contexto)

def viaje_listo(request):
	return render(request, 'viaje/listo.html')

def Viajelist(request):
	for v in Viaje.objects.all():
		lista = []
		if v.conductor == request.user._conductor:
			lista.append(v)
	return render(request, 'viaje/viaje_list.html', {'viajes':lista})


