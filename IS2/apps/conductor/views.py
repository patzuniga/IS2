from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

#def index(request):
#	return render(request,'conductor/index.html')

def configuracion(request):
	return render(request, 'conductor/configuracion.html')