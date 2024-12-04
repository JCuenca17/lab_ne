from django import forms
from .models import MaestroEquipo
from django.contrib.auth.forms import AuthenticationForm


class MaestroForm(forms.ModelForm):
    class Meta:
        model = MaestroEquipo
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
