from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.core.validators import FileExtensionValidator
import os

def evento_pdf_path(instance, filename):
    """Generar ruta para archivos PDF de eventos usando la clave de dependencia."""
    dependencia_identificador = "sin_dependencia"
    if instance.usuario_creador and instance.usuario_creador.dependencia:
        # Usar cve_dep (un entero) como string para el nombre de la carpeta
        dependencia_identificador = str(instance.usuario_creador.dependencia.cve_dep)
    return f'eventos/{dependencia_identificador}/{filename}'

class Titular(models.Model):
    """Modelo para los titulares de las dependencias"""
    cve_titular = models.IntegerField(primary_key=True, verbose_name='Clave del Titular')
    nom_titular = models.CharField(max_length=255, verbose_name='Nombre del Titular')

    class Meta:
        verbose_name = 'Titular'
        verbose_name_plural = 'Titulares'
        ordering = ['nom_titular']

    def __str__(self):
        return self.nom_titular

class Dependencia(models.Model):
    """Modelo para las dependencias gubernamentales"""
    cve_dep = models.IntegerField(primary_key=True, verbose_name='Clave de la Dependencia')
    nom_dep = models.CharField(max_length=255, verbose_name='Nombre de la Dependencia')
    old_titular = models.CharField(max_length=255, verbose_name='Titular de la Dependencia (old)', blank=True, null=True) # Renamed for clarity
    titular_fk = models.ForeignKey(Titular, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Titular de la Dependencia') # New FK field

    class Meta:
        verbose_name = 'Dependencia'
        verbose_name_plural = 'Dependencias'
        ordering = ['nom_dep']

    def __str__(self):
        return self.nom_dep

class CustomUser(AbstractUser):
    """Usuario personalizado con información de dependencias gubernamentales"""
    
    GENDER_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
    ]
    
    USER_TYPE_CHOICES = [
        ('captura', 'Usuario de Captura'),
        ('admin', 'Administrador'),
    ]
    
    # Campos adicionales requeridos
    dependencia = models.ForeignKey(Dependencia, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Dependencia')
    nombre_completo = models.CharField(max_length=100, verbose_name='Nombre Completo del Usuario')
    direccion = models.TextField(verbose_name='Dirección')
    genero = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name='Género')
    tipo_usuario = models.CharField(
        max_length=10, 
        choices=USER_TYPE_CHOICES, 
        default='captura',
        verbose_name='Tipo de Usuario'
    )
    
    # Sobreescribir is_active para control de estado
    is_active = models.BooleanField(default=True, verbose_name='Cuenta Activa')
    
    class Meta:
        verbose_name = 'Usuario del Sistema'
        verbose_name_plural = 'Usuarios del Sistema'
    
    def __str__(self):
        return f"{self.nombre_completo} - {self.dependencia.nom_dep if self.dependencia else 'Sin dependencia'}"
    
    def is_admin_user(self):
        """Verificar si es usuario administrador"""
        return self.tipo_usuario == 'admin'
    
    def is_captura_user(self):
        """Verificar si es usuario de captura"""
        return self.tipo_usuario == 'captura'


class Municipio(models.Model):
    """Modelo para los municipios"""
    cve_mun = models.IntegerField(primary_key=True, verbose_name='Clave del Municipio')
    nom_mun = models.CharField(max_length=255, verbose_name='Nombre del Municipio')

    class Meta:
        verbose_name = 'Municipio'
        verbose_name_plural = 'Municipios'
        ordering = ['nom_mun']

    def __str__(self):
        return self.nom_mun


class Evento(models.Model):
    """Modelo para eventos gubernamentales"""
    
    ESTADO_CHOICES = [
        ('programado', 'Programado'),
        ('revisado', 'Revisado'),
        ('activo', 'Activo'),
        ('finalizado', 'Finalizado'),
        ('cancelado', 'Cancelado'),
    ]
    
    ASISTENCIA_GOBERNADOR_CHOICES = [
        (True, 'Sí'),
        (False, 'No'),
    ]
    
    # Campos principales del evento
    nombre_evento = models.CharField(max_length=200, verbose_name='Nombre del Evento')
    observaciones = models.TextField(blank=True, null=True, verbose_name='Descripción')
    lugar_evento = models.CharField(max_length=200, verbose_name='Lugar del Evento', blank=True, null=True)
    numero_documento = models.CharField(max_length=50, verbose_name='Número del Documento', blank=True, null=True)
    asistira_gobernador = models.BooleanField(choices=ASISTENCIA_GOBERNADOR_CHOICES, default=False, verbose_name='¿Asistirá el Gobernador?', blank=True, null=True)
    anotaciones = models.TextField(blank=True, null=True, verbose_name='Anotaciones (Admin)')
    archivo_respuesta_admin = models.FileField(upload_to=evento_pdf_path, validators=[FileExtensionValidator(['pdf'])], verbose_name='Archivo de Respuesta (Admin)', blank=True, null=True)
    
    # Campos de relación y estado
    usuario_creador = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name='eventos_creados', verbose_name='Usuario Creador')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='programado', verbose_name='Estado del Evento')
    
    # Campos de fecha y hora
    fecha_hora_inicio = models.DateTimeField(verbose_name='Fecha y Hora de Inicio')
    fecha_hora_fin = models.DateTimeField(verbose_name='Fecha y Hora de Fin', blank=True, null=True)
    
    # Campos de auditoría
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name='Última Actualización')
    
    archivo_pdf = models.FileField(upload_to=evento_pdf_path, validators=[FileExtensionValidator(['pdf'])], verbose_name='Archivo PDF', blank=True, null=True)
    municipio = models.ForeignKey(Municipio, on_delete=models.PROTECT, verbose_name='Municipio', default=101)

    @property
    def dependencia(self):
        return self.usuario_creador.dependencia.nom_dep if self.usuario_creador.dependencia else ""

    @property
    def titular(self):
        return self.usuario_creador.dependencia.titular_fk.nom_titular if self.usuario_creador.dependencia and self.usuario_creador.dependencia.titular_fk else ""

    def __str__(self):
        return self.nombre_evento

class LogEventoEstado(models.Model):
    """Modelo para registrar los cambios de estado de un evento."""
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name='logs_estado')
    estado_anterior = models.CharField(max_length=20, choices=Evento.ESTADO_CHOICES, null=True, blank=True)
    estado_nuevo = models.CharField(max_length=20, choices=Evento.ESTADO_CHOICES)
    usuario_cambio = models.ForeignKey(
        CustomUser, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name='Usuario que realizó el cambio'
    )
    fecha_cambio = models.DateTimeField(auto_now_add=True, verbose_name='Fecha del cambio')
    comentario = models.TextField(blank=True, null=True, verbose_name='Comentario adicional')
    automatico = models.BooleanField(default=False, verbose_name='Cambio automático')

    class Meta:
        verbose_name = 'Log de Estado de Evento'
        verbose_name_plural = 'Logs de Estados de Eventos'
        ordering = ['-fecha_cambio']

    def __str__(self):
        return f'Log para {self.evento.nombre_evento} - {self.fecha_cambio.strftime("%Y-%m-%d %H:%M")}'