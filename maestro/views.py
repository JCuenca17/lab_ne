from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import MaestroEquipo
from .forms import MaestroForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required
# Create your views here.


def inicio(request):
    return render(request, 'pages/inicio.html')


def nosotros(request):
    return render(request, 'pages/nosotros.html')

@login_required(login_url='login')
def maestros(request):
    query = request.GET.get('search', '')  # Obtiene la consulta de búsqueda
    filtro = ''  # Inicializa filtro con un valor predeterminado

    if query:
        maestros = MaestroEquipo.objects.filter(
            Q(id__icontains=query) |
            Q(nombre__icontains=query) |
            Q(ubicacion__icontains=query)
        )
    else:
        # Obtiene el filtro de los parámetros de la URL
        filtro = request.GET.get('filtro', 'activos')
        if filtro == 'eliminados':
            maestros = MaestroEquipo.objects.filter(estado_registro='*')
        elif filtro == 'inactivos':
            maestros = MaestroEquipo.objects.filter(estado_registro='I')
        else:  # Por defecto, mostrar activos
            maestros = MaestroEquipo.objects.filter(estado_registro='A')

    # Renderiza la plantilla con los datos necesarios
    return render(request, 'maestro/index.html', {'maestros': maestros, 'filtro': filtro, 'query': query})

@login_required(login_url='login')
def crear(request):
    formulario = MaestroForm(request.POST or None)
    if formulario.is_valid():
        formulario.save()
        return redirect('maestro')
    return render(request, 'maestro/crear.html', {'formulario': formulario})

@login_required(login_url='login')
def editar(request, id):
    maestros = MaestroEquipo.objects.get(id=id)
    formulario = MaestroForm(request.POST or None, instance=maestros)
    if formulario.is_valid() and request.method == 'POST':
        formulario.save()
        return redirect('maestro')
    return render(request, 'maestro/editar.html', {'formulario': formulario})

@login_required(login_url='login')
def eliminar(request, id):
    maestros = MaestroEquipo.objects.get(id=id)
    # maestros.delete()
    maestros.estado_registro = '*'
    maestros.save()
    return redirect('maestro')

@login_required(login_url='login')
def activar(request, id):
    maestro = MaestroEquipo.objects.get(id=id)
    maestro.estado_registro = 'A'  # Cambiar a activo
    maestro.save()
    return redirect('maestro')

@login_required(login_url='login')
def desactivar(request, id):
    maestro = MaestroEquipo.objects.get(id=id)
    maestro.estado_registro = 'I'  # Cambiar a inactivo
    maestro.save()
    return redirect('maestro')
