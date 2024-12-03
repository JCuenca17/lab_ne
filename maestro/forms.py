from django import forms
from .models import MaestroEquipo


class MaestroForm(forms.ModelForm):
    class Meta:
        model = MaestroEquipo
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            # Si estamos editando, solo permitir 'Activo' o 'Inactivo' para el campo estado_registro
        if self.instance.pk:
            self.fields['estado_registro'].choices = [
                ('A', 'Activo'),
                ('I', 'Inactivo')
            ]
        # Si no hay instancia (crear), el campo es solo lectura y tiene el valor por defecto
        if not self.instance.pk:
            self.fields['estado_registro'].widget.attrs['readonly'] = True
            self.fields['estado_registro'].initial = 'A'
