from django.shortcuts import render, redirect
from django.http import HttpResponse

from apps.viaje.forms import ViajeForm
from apps.viaje.models import Viaje
from django.views.generic import ListView

def index(request):
	return render(request,'viaje/index.html')

def viaje_view(request):
	if request.method == 'POST':
		form = ViajeForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('viaje:index')
	else:
		form = ViajeForm()
	return render(request,'viaje/viaje_form.html',{'form':form})

def viaje_list(request):
	viaje = Viaje.objects.all()
	contexto = {'viajes':viaje}
	return render(request, 'viaje/viaje_list.html', contexto)

class Viajelist(ListView):
	model = Viaje
	template_name ='viaje/viaje_list.html'
