# forms.py

from django import forms
from .models import MaestroEquipo, TallerMantenimiento, TipoEquipo
from django.contrib.auth.forms import AuthenticationForm


class MaestroForm(forms.ModelForm):
    class Meta:
        model = MaestroEquipo
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

        # Filtrar los datos relacionados para incluir solo activos
        if 'taller_mantenimiento' in self.fields:
            self.fields['taller_mantenimiento'].queryset = TallerMantenimiento.objects.filter(
                estado_registro='A')

        if 'tipo_equipo' in self.fields:
            self.fields['tipo_equipo'].queryset = TipoEquipo.objects.filter(
                estado_registro='A')

        # Eliminar 'estado_registro' del formulario
        if 'estado_registro' in self.fields:
            del self.fields['estado_registro']


class TallerForm(forms.ModelForm):
    class Meta:
        model = TallerMantenimiento
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

        # Eliminar 'estado_registro' del formulario
        if 'estado_registro' in self.fields:
            del self.fields['estado_registro']


class TipoForm(forms.ModelForm):
    class Meta:
        model = TipoEquipo
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

        # Eliminar 'estado_registro' del formulario
        if 'estado_registro' in self.fields:
            del self.fields['estado_registro']


class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
