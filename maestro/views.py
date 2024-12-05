from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import MaestroEquipo, TallerMantenimiento, TipoEquipo
from .forms import MaestroForm, TallerForm, TipoForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required
# Create your views here.


def inicio(request):
    return render(request, 'pages/inicio.html')


@login_required(login_url='login')
def tablas(request):
    return render(request, 'pages/tablas.html')


MODELOS = {
    'maestro': {
        'model': MaestroEquipo,
        'filters': ['activos', 'inactivos', 'eliminados'],
        'additional_filters': ['taller', 'tipo'],
        'template': 'maestro/index.html',
        'related_models': {
            'taller': TallerMantenimiento,
            'tipo': TipoEquipo
        },
        'form': MaestroForm,
        'url': 'maestro'
    },
    'taller': {
        'model': TallerMantenimiento,
        'filters': ['activos', 'inactivos', 'eliminados'],
        'template': 'taller/index.html',
        'related_models': {},
        'form': TallerForm,
        'url': 'taller'
    },
    'tipo': {
        'model': TipoEquipo,
        'filters': ['activos', 'inactivos', 'eliminados'],
        'template': 'tipo/index.html',
        'related_models': {},
        'form': TipoForm,
        'url': 'tipo'
    },
}


@login_required(login_url='login')
def listar(request, modelo):
    # Obtener la configuración del modelo
    modelo_config = MODELOS.get(modelo)
    if not modelo_config:
        return render(request, 'error.html', {'message': 'Modelo no encontrado'})

    # Obtener los parámetros de búsqueda y filtros
    query = request.GET.get('search', '')
    filtros = request.GET.getlist('filtro')
    filtro_seleccionado = {}

    # Obtener los filtros adicionales (si aplican)
    additional_filters = modelo_config.get('additional_filters', [])
    for filtro in additional_filters:
        filtro_seleccionado[filtro] = request.GET.getlist(filtro)

    # Filtro por búsqueda
    if query:
        q_filter = Q()
        # Agregar búsqueda genérica por campo (solo si esos campos existen en el modelo)
        if hasattr(modelo_config['model'], 'id'):
            q_filter |= Q(id__icontains=query)
        if hasattr(modelo_config['model'], 'nombre'):
            q_filter |= Q(nombre__icontains=query)
        if hasattr(modelo_config['model'], 'ubicacion'):
            q_filter |= Q(ubicacion__icontains=query)

        objetos = modelo_config['model'].objects.filter(q_filter)
    else:
        # Filtro de estado
        query_filtro = Q()
        for filtro in modelo_config['filters']:
            if filtro in filtros:
                if filtro == 'activos':
                    query_filtro |= Q(estado_registro='A')
                elif filtro == 'inactivos':
                    query_filtro |= Q(estado_registro='I')
                elif filtro == 'eliminados':
                    query_filtro |= Q(estado_registro='*')

        objetos = modelo_config['model'].objects.filter(query_filtro)

    # Aplicar filtros adicionales si existen (ej. taller, tipo)
    for filtro, valores in filtro_seleccionado.items():
        if valores:
            if filtro == 'taller':  # Filtrar por taller
                objetos = objetos.filter(taller_mantenimiento__id__in=valores)
            elif filtro == 'tipo':  # Filtrar por tipo
                objetos = objetos.filter(tipo_equipo__id__in=valores)
            else:
                objetos = objetos.filter(**{f'{filtro}__id__in': valores})

    # Obtener los modelos relacionados (como Talleres, Tipos)
    modelos_relacionados = {}
    for filtro, related_model in modelo_config['related_models'].items():
        modelos_relacionados[filtro] = related_model.objects.all()

    # Renderizar la plantilla con los objetos obtenidos
    return render(request, modelo_config['template'], {
        'objetos': objetos,
        'filtro': filtros,
        'query': query,
        'modelo_nombre': modelo,
        'modelos_relacionados': modelos_relacionados,
        'filtro_seleccionado': filtro_seleccionado,
    })


@login_required(login_url='login')
def crear(request, modelo):
    # Obtener la configuración del modelo
    modelo_config = MODELOS.get(modelo)
    if not modelo_config:
        return render(request, 'error.html', {'message': 'Modelo no encontrado'})

    # Obtener el formulario correspondiente
    formulario = modelo_config['form'](request.POST or None)

    if formulario.is_valid():
        formulario.save()
        return redirect(modelo_config['url'])

    return render(request, 'crear.html', {'formulario': formulario})


@login_required(login_url='login')
def editar(request, modelo, id):
    # Obtener la configuración del modelo
    modelo_config = MODELOS.get(modelo)
    if not modelo_config:
        return render(request, 'error.html', {'message': 'Modelo no encontrado'})

    # Obtener el modelo y el formulario correspondiente
    model_class = modelo_config['model']
    form_class = modelo_config['form']

    # Intentar obtener el objeto a editar
    try:
        objeto = model_class.objects.get(id=id)
    except model_class.DoesNotExist:
        return render(request, 'error.html', {'message': 'Objeto no encontrado'})

    # Crear el formulario con los datos del objeto
    formulario = form_class(request.POST or None, instance=objeto)

    if formulario.is_valid() and request.method == 'POST':
        formulario.save()
        # Redirigir al listado correspondiente
        return redirect(modelo_config['url'])

    # Renderizar la plantilla con el formulario
    return render(request, 'editar.html', {
        'formulario': formulario,
        'objeto': objeto,
        'modelo_nombre': modelo
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
def detalle(request, modelo, id):
    # Obtener la configuración del modelo
    modelo_config = MODELOS.get(modelo)
    if not modelo_config:
        return render(request, 'error.html', {'message': 'Modelo no encontrado'})

    # Obtener el modelo correspondiente de la configuración
    model_class = modelo_config['model']

    # Intentar obtener el objeto
    try:
        objeto = model_class.objects.get(id=id)
    except model_class.DoesNotExist:
        return render(request, 'error.html', {'message': 'Objeto no encontrado'})

    # Crear un diccionario con los campos disponibles del objeto
    campos_objeto = {}
    for field in objeto._meta.get_fields():
        # Si el campo existe, lo añadimos al diccionario
        campo_name = field.name
        if hasattr(objeto, campo_name):
            campos_objeto[campo_name] = getattr(objeto, campo_name)

    # Renderizar el template con el objeto y sus campos
    return render(request, 'detalle.html', {
        'objeto': objeto,
        'modelo_nombre': modelo,
        'campos_objeto': campos_objeto,
    })
