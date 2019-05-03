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
			login(request, user)
			return render(request,'login/base.html',{})
		else:
			return render(request, 'login/login.html',{})
	return render(request,'login/login.html',{})