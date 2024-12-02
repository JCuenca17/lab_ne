from django import forms
from .models import MaestroEquipo


class MaestroForm(forms.ModelForm):       
    class Meta:
        model = MaestroEquipo
        fields = '__all__'

