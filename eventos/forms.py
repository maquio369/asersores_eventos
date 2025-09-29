from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Evento, CustomUser, Municipio, Dependencia
import os

class EventoForm(forms.ModelForm):
    """Formulario para crear y editar eventos"""
    
    class Meta:
        model = Evento
        fields = [
            'nombre_evento', 'observaciones', 'lugar_evento', 'numero_documento',
            'fecha_hora_inicio', 'fecha_hora_fin', 'asistira_gobernador',
            'archivo_pdf', 'municipio', 'anotaciones', 'archivo_respuesta_admin',
            'estado'
        ]
        
        widgets = {
            'nombre_evento': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Inauguración de obra pública'
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Descripción detallada del evento',
                'rows': 3
            }),
            'lugar_evento': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Plaza Principal, Centro de la Ciudad'
            }),
            'numero_documento': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: OF-2025-001'
            }),
            'fecha_hora_inicio': forms.DateTimeInput(
                attrs={'class': 'form-control', 'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            ),
            'fecha_hora_fin': forms.DateTimeInput(
                attrs={'class': 'form-control', 'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            ),
            'asistira_gobernador': forms.RadioSelect(attrs={
                'class': 'btn-check'
            }),
            'archivo_pdf': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf'
            }),
            'municipio': forms.Select(attrs={
                'class': 'form-select',
            }),
            'anotaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Anotaciones internas para el administrador',
                'rows': 3
            }),
            'archivo_respuesta_admin': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf'
            }),
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }
        
        labels = {
            'nombre_evento': 'Nombre del Evento *',
            'observaciones': 'Descripción',
            'lugar_evento': 'Lugar del Evento',
            'numero_documento': 'Número del Documento',
            'fecha_hora_inicio': 'Fecha y Hora de Inicio *',
            'fecha_hora_fin': 'Fecha y Hora de Finalización',
            'asistira_gobernador': '¿Asistirá el Gobernador?',
            'archivo_pdf': 'Documento PDF Informativo',
            'municipio': 'Municipio *',
            'anotaciones': 'Anotaciones (Admin)',
            'archivo_respuesta_admin': 'Archivo de Respuesta (Admin)',
            'estado': 'Estado del Evento',
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Configurar ayuda contextual
        self.fields['archivo_pdf'].help_text = 'Solo archivos PDF, máximo 5MB'
        self.fields['fecha_hora_inicio'].help_text = 'Selecciona fecha y hora de inicio del evento'
        self.fields['fecha_hora_fin'].help_text = 'Opcional. Si se deja en blanco, se asignará el fin del día.'
        self.fields['archivo_respuesta_admin'].help_text = 'Solo archivos PDF, máximo 5MB'

        # Si el usuario no es administrador, ocultar campos de admin
        if self.user and not self.user.is_admin_user():
            admin_fields = ['asistira_gobernador', 'anotaciones', 'archivo_respuesta_admin', 'estado']
            for field_name in admin_fields:
                if field_name in self.fields:
                    del self.fields[field_name]
    
    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get('fecha_hora_inicio')
        fecha_fin = cleaned_data.get('fecha_hora_fin')

        # Si no hay fecha de inicio, no podemos validar nada más
        if not fecha_inicio:
            return cleaned_data

        # Lógica para auto-completar fecha_fin
        if not fecha_fin:
            cleaned_data['fecha_hora_fin'] = fecha_inicio.replace(hour=23, minute=59, second=59)
            fecha_fin = cleaned_data['fecha_hora_fin'] # Actualizar la variable local

        # Validar que la fecha de fin sea posterior al inicio
        if fecha_fin <= fecha_inicio:
            self.add_error('fecha_hora_fin', 'La fecha de finalización debe ser posterior a la fecha de inicio.')

        # Validar que no sea muy largo (máximo 24 horas)
        diferencia = fecha_fin - fecha_inicio
        if diferencia.total_seconds() > 86400:  # 24 horas
            self.add_error('fecha_hora_fin', 'El evento no puede durar más de 24 horas.')

        return cleaned_data

    def clean_fecha_hora_inicio(self):
        """Validar que la fecha de inicio sea futura, excepto en la edición."""
        fecha_inicio = self.cleaned_data.get('fecha_hora_inicio')

        # Si es un formulario de edición (self.instance.pk existe), no validar.
        if self.instance and self.instance.pk:
            return fecha_inicio

        if fecha_inicio:
            ahora = timezone.now()
            if fecha_inicio <= ahora:
                raise ValidationError(
                    'La fecha de inicio debe ser posterior a la fecha actual.'
                )
        
        return fecha_inicio

    
    
    def clean_archivo_pdf(self):
        """Validar archivo PDF"""
        archivo = self.cleaned_data.get('archivo_pdf')
        
        if archivo:
            # Validar extensión
            nombre_archivo = archivo.name.lower()
            if not nombre_archivo.endswith('.pdf'):
                raise ValidationError('Solo se permiten archivos PDF.')
            
            # Validar tamaño (5MB máximo)
            if archivo.size > 5 * 1024 * 1024:
                raise ValidationError('El archivo no puede ser mayor a 5MB.')
        
        return archivo
    
    def clean_archivo_respuesta_admin(self):
        """Validar archivo PDF de respuesta del admin"""
        archivo = self.cleaned_data.get('archivo_respuesta_admin')
        
        if archivo:
            # Validar extensión
            nombre_archivo = archivo.name.lower()
            if not nombre_archivo.endswith('.pdf'):
                raise ValidationError('Solo se permiten archivos PDF.')
            
            # Validar tamaño (5MB máximo)
            if archivo.size > 5 * 1024 * 1024:
                raise ValidationError('El archivo no puede ser mayor a 5MB.')
        
        return archivo
    
    def save(self, commit=True):
        """
        Guardar evento.
        Asigna el usuario creador solo si es un evento nuevo.
        """
        evento = super().save(commit=False)
        
        # Si el evento es nuevo (no tiene pk), se le asigna el usuario creador.
        if not self.instance.pk and self.user:
            evento.usuario_creador = self.user
        
        if commit:
            evento.save()
        
        return evento

class FiltroEventosForm(forms.Form):
    """Formulario para filtrar eventos"""
    
    ESTADO_CHOICES = [
        ('', 'Todos los estados'),
        ('programado', 'Programado'),
        ('activo', 'Activo'),
        ('finalizado', 'Finalizado'),
        ('cancelado', 'Cancelado'),
    ]
    
    GOBERNADOR_CHOICES = [
        ('', 'Cualquier opción'),
        ('True', 'Sí asistirá'),
        ('False', 'No asistirá'),
    ]
    
    busqueda = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por nombre, lugar o documento...'
        })
    )
    
    estado = forms.ChoiceField(
        choices=ESTADO_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    asistira_gobernador = forms.ChoiceField(
        choices=GOBERNADOR_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    fecha_desde = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    fecha_hasta = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )

    municipio = forms.ModelChoiceField(
        queryset=Municipio.objects.all().order_by('nom_mun'),
        required=False,
        empty_label="Todos los municipios",
        widget=forms.Select(attrs={'class': 'form-select form-select-sm'})
    )

    dependencia = forms.ModelChoiceField(
        queryset=Dependencia.objects.all().order_by('nom_dep'),
        required=False,
        empty_label="Todas las dependencias",
        widget=forms.Select(attrs={'class': 'form-select form-select-sm'})
    )


