from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from .forms import CustomLoginForm
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('tablas/', views.tablas, name='tablas'),
    path('maestro/', views.listar, {'modelo': 'maestro'}, name='maestro'),
    path('taller/', views.listar, {'modelo': 'taller'}, name='taller'),
    path('tipo/', views.listar, {'modelo': 'tipo'}, name='tipo'),
    path('<str:modelo>/crear/', views.crear, name='crear'),
    path('<str:modelo>/editar/<str:id>/', views.editar, name='editar'),
    path('<str:modelo>/detalle/<str:id>/', views.detalle, name='detalle'),
    path('eliminar/<str:modelo>/<str:id>/', views.eliminar, name='eliminar'),
    path('activar/<str:modelo>/<str:id>/', views.activar, name='activar'),
    path('desactivar/<str:modelo>/<str:id>/',
         views.desactivar, name='desactivar'),
    path('login/', LoginView.as_view(template_name='pages/login.html',
         authentication_form=CustomLoginForm), name='login'),
    path('logout/', LogoutView.as_view(next_page='inicio'), name='logout'),
    path('', include('pwa.urls')),
]
