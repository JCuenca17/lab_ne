from django.db import models


class TipoEquipo(models.Model):
    id = models.CharField(
        max_length=10,
        unique=True,
        primary_key=True,
        verbose_name="ID del Tipo de Equipo"
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


class TallerMantenimiento(models.Model):
    id = models.CharField(
        max_length=10,
        unique=True,
        primary_key=True,
        verbose_name="ID del Taller"
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


class MaestroEquipo(models.Model):
    id = models.CharField(
        max_length=10,
        unique=True,
        primary_key=True,  # Indica que es clave primaria
        verbose_name="ID del Equipo"
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
        choices=[
            ('A', 'Activo'),
            ('I', 'Inactivo'),
            ('*', 'Eliminado')
        ],
        default='A',
        verbose_name="Estado de Registro"
    )

    class Meta:
        verbose_name = "Maestro de Equipo"
        verbose_name_plural = "Maestros de Equipos"
        ordering = ['id']

    def __str__(self):
        return f"{self.nombre} ({self.id})"
