from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from apps.conductor.models import Conductor
from apps.usuario.models import Usuario

@login_required()
def configuracion(request):
	#current_user = request.user
	print("A")
	u = Usuario.objects.get(id=request.user.pk)
	conductor = u.conductor_set.all()[0]
	auto_a = conductor.autoaceptar_reservas
#	if request.method == 'POST':
#		print("B")
#		auto_a = not auto_a
#		conductor.autoaceptar_reservas = auto_a
#		conductor.save()
	return render(request, 'conductor/configuracion.html',{'auto_a':auto_a})

@login_required()
def cambio(request):
	print("C")
	u = Usuario.objects.get(id=request.user.pk)
	conductor = u.conductor_set.all()[0]
	auto_a = conductor.autoaceptar_reservas
	if request.method == 'POST':
		print("D")
		auto_a = not auto_a
		conductor.autoaceptar_reservas = auto_a
		conductor.save()
#	return configuracion(request) #render(request, 'conductor/configuracion.html',{'auto_a':auto_a})
	return HttpResponseRedirect('/conductor/configuracion/')