from django.contrib import admin
from .models import MaestroEquipo, TallerMantenimiento, TipoEquipo

# Register your models here.
admin.site.register(MaestroEquipo)
admin.site.register(TallerMantenimiento)
admin.site.register(TipoEquipo)