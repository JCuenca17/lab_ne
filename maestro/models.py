from django.db import models
from django.db.models import Max
from django.db.models.signals import pre_save
from django.dispatch import receiver


def generar_id_secuencial(prefijo, modelo, longitud=5):
    # Encuentra el último valor del ID para ese modelo (por ejemplo, 'TE_00023')
    ultimo_id = modelo.objects.aggregate(Max('id'))['id__max']

    if ultimo_id:
        # Extraemos solo los números del último ID generado
        try:
            # Solo los números
            numero_actual = int(
                ''.join(filter(str.isdigit, ultimo_id[len(prefijo):])))
        except ValueError:
            numero_actual = 0  # Si no se puede convertir, empieza desde 0
    else:
        numero_actual = 0

    # Incrementa el número para el nuevo ID
    nuevo_numero = numero_actual + 1

    # Genera el nuevo ID con el prefijo y el número secuencial
    nuevo_id = f"{prefijo}{str(nuevo_numero).zfill(longitud)}"

    return nuevo_id


class TipoEquipo(models.Model):
    id = models.CharField(
        max_length=10,
        unique=True,
        primary_key=True,
        verbose_name="ID del Tipo de Equipo",
        editable=False  # No editable
    )
    nombre = models.CharField(
        max_length=100,
        verbose_name="Nombre del Tipo de Equipo"
    )
    estado_registro = models.CharField(
        max_length=1,
        choices=[('A', 'Activo'), ('I', 'Inactivo'), ('*', 'Eliminado')],
        default='A',
        verbose_name="Estado de Registro"
    )

    class Meta:
        verbose_name = "Tipo de Equipo"
        verbose_name_plural = "Tipos de Equipos"

    def __str__(self):
        return f"{self.nombre} ({self.id})"


@receiver(pre_save, sender=TipoEquipo)
def set_tipo_equipo_id(sender, instance, **kwargs):
    if not instance.id:
        instance.id = generar_id_secuencial(
            'TE_', TipoEquipo)  # Genera el ID secuencial

# Similar para el modelo TallerMantenimiento


class TallerMantenimiento(models.Model):
    id = models.CharField(
        max_length=10,
        unique=True,
        primary_key=True,
        verbose_name="ID del Taller",
        editable=False  # No editable
    )
    nombre = models.CharField(
        max_length=100,
        verbose_name="Nombre del Taller"
    )
    estado_registro = models.CharField(
        max_length=1,
        choices=[('A', 'Activo'), ('I', 'Inactivo'), ('*', 'Eliminado')],
        default='A',
        verbose_name="Estado de Registro"
    )

    class Meta:
        verbose_name = "Taller de Mantenimiento"
        verbose_name_plural = "Talleres de Mantenimiento"

    def __str__(self):
        return f"{self.nombre} ({self.id})"


@receiver(pre_save, sender=TallerMantenimiento)
def set_taller_mantenimiento_id(sender, instance, **kwargs):
    if not instance.id:
        instance.id = generar_id_secuencial(
            'TM_', TallerMantenimiento)  # Genera el ID secuencial

# Para el modelo MaestroEquipo


class MaestroEquipo(models.Model):
    id = models.CharField(
        max_length=10,
        unique=True,
        primary_key=True,
        verbose_name="ID del Equipo",
        editable=False  # No editable
    )
    nombre = models.CharField(
        max_length=100,
        verbose_name="Nombre del Equipo"
    )
    taller_mantenimiento = models.ForeignKey(
        TallerMantenimiento,
        on_delete=models.CASCADE,
        related_name="equipos",
        verbose_name="Taller de Mantenimiento"
    )
    tipo_equipo = models.ForeignKey(
        TipoEquipo,
        on_delete=models.CASCADE,
        related_name="equipos",
        verbose_name="Tipo de Equipo"
    )
    ubicacion = models.CharField(
        max_length=200,
        verbose_name="Ubicación"
    )
    estado_registro = models.CharField(
        max_length=1,
        choices=[('A', 'Activo'), ('I', 'Inactivo'), ('*', 'Eliminado')],
        default='A',
        verbose_name="Estado de Registro"
    )

    class Meta:
        verbose_name = "Maestro de Equipo"
        verbose_name_plural = "Maestros de Equipos"
        ordering = ['id']

    def __str__(self):
        return f"{self.nombre} ({self.id})"


@receiver(pre_save, sender=MaestroEquipo)
def set_maestro_equipo_id(sender, instance, **kwargs):
    if not instance.id:
        instance.id = generar_id_secuencial(
            'ME_', MaestroEquipo)  # Genera el ID secuencial
