from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login


def index(request):
	return HttpResponse("tsupalo diego")

def my_view(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			print(request.POST)
			if(request.POST["tipo"] == "conductor"):
				try:
  					user._conductor
  					login(request, user)
  					return render(request, 'login/base2.html',{})
				except:
					return render(request, 'login/login.html',{})

			elif(request.POST["tipo"] == "pasajero"):
				login(request, user)
				return render(request, 'usuario/index.html',{})
			else:
				return render(request, 'login/login.html',{})
		else:
			return render(request, 'login/login.html',{})
	return render(request,'login/login.html',{})