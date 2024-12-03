from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('nosotros', views.nosotros, name='nosotros'),
    # path('maestro', views.maestros, name='maestro'),
    path('maestro/', views.maestros, name='maestro'),
    path('maestro/crear', views.crear, name='crear'),
    path('maestro/editar', views.editar, name='editar'),
    path('eliminar/<str:id>', views.eliminar, name='eliminar'),
    path('maestro/editar/<str:id>', views.editar, name='editar'),
    path('desactivar/<str:id>/', views.desactivar, name='desactivar'),
    path('activar/<str:id>/', views.activar, name='activar'),
    path('', include('pwa.urls')),
]
