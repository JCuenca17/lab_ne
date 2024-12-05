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
    # Obtiene todos los filtros seleccionados
    filtros = request.GET.getlist('filtro')

    # Filtrado por búsqueda
    if query:
        maestros = MaestroEquipo.objects.filter(
            Q(id__icontains=query) |
            Q(nombre__icontains=query) |
            Q(ubicacion__icontains=query)
        )
    else:
        if filtros:
            # Inicializamos el filtro base con un Q() vacío
            query_filtro = Q()
            if 'activos' in filtros:
                query_filtro |= Q(estado_registro='A')
            if 'inactivos' in filtros:
                query_filtro |= Q(estado_registro='I')
            if 'eliminados' in filtros:
                query_filtro |= Q(estado_registro='*')

            maestros = MaestroEquipo.objects.filter(query_filtro)
        else:
            # Si no hay filtros seleccionados, mostramos todos los registros
            maestros = MaestroEquipo.objects.all()

    # Renderiza la plantilla con los datos necesarios
    return render(request, 'maestro/index.html', {'maestros': maestros, 'filtro': filtros, 'query': query})


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
    return render(request, 'maestro/editar.html', {
        'formulario': formulario,
        'maestro': maestros
    })


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


@login_required(login_url='login')
def detalle(request, id):
    maestro = MaestroEquipo.objects.get(id=id)
    return render(request, 'maestro/detalle.html', {'maestro': maestro})
