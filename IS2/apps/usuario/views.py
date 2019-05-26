from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from apps.usuario.models import Usuario

@login_required()
def home(request):
	if request.user.is_authenticated is not None:
		try:
			current_user = request.user
			u = Usuario.objects.get(id=current_user.id)
			u.conductor_set.all()[0]
			return render(request, 'usuario/index2.html',{})
		except:
			return render(request, 'usuario/index.html',{})
