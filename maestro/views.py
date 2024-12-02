from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import MaestroEquipo
from .forms import MaestroForm
# Create your views here.

def inicio(request):
    return render(request, 'pages/inicio.html')

def nosotros(request):
    return render(request, 'pages/nosotros.html')

def maestros(request):
    maestros = MaestroEquipo.objects.all()
    return render(request, 'maestro/index.html', {'maestros': maestros})

def crear(request):
    formulario = MaestroForm(request.POST or None)
    if formulario.is_valid():
        formulario.save()
        return redirect('maestro')
    return render(request, 'maestro/crear.html', {'formulario': formulario})

def editar(request, id):
    maestros = MaestroEquipo.objects.get(id=id)
    formulario = MaestroForm(request.POST or None, instance=maestros)
    if formulario.is_valid() and request.method == 'POST':
        formulario.save()
        return redirect('maestro')
    return render(request, 'maestro/editar.html', {'formulario': formulario})

def eliminar(request, id):
    maestros = MaestroEquipo.objects.get(id=id)
    maestros.delete()
    return redirect('maestro')

