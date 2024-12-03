from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import MaestroEquipo
from .forms import MaestroForm
# Create your views here.


def inicio(request):
    return render(request, 'pages/inicio.html')


def nosotros(request):
    return render(request, 'pages/nosotros.html')


""" def maestros(request):
    maestros = MaestroEquipo.objects.all()
    #maestros = MaestroEquipo.objects.filter(estado_registro='A')
    return render(request, 'maestro/index.html', {'maestros': maestros}) """


def maestros(request):
    # Por defecto, mostrar activos
    filtro = request.GET.get('filtro', 'activos')
    if filtro == 'eliminados':
        maestros = MaestroEquipo.objects.filter(estado_registro='*')
    elif filtro == 'inactivos':
        maestros = MaestroEquipo.objects.filter(estado_registro='I')
    else:  # Por defecto, mostrar activos
        maestros = MaestroEquipo.objects.filter(estado_registro='A')

    return render(request, 'maestro/index.html', {'maestros': maestros, 'filtro': filtro})


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
    # maestros.delete()
    maestros.estado_registro = '*'
    maestros.save()
    return redirect('maestro')


def activar(request, id):
    maestro = MaestroEquipo.objects.get(id=id)
    maestro.estado_registro = 'A'  # Cambiar a activo
    maestro.save()
    return redirect('maestro')


def desactivar(request, id):
    maestro = MaestroEquipo.objects.get(id=id)
    maestro.estado_registro = 'I'  # Cambiar a inactivo
    maestro.save()
    return redirect('maestro')
