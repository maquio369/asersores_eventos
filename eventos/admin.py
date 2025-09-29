from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Evento, LogEventoEstado, Dependencia, Titular # Added Titular

@admin.register(Titular) # Register Titular model
class TitularAdmin(admin.ModelAdmin):
    """Administrador para Titulares"""
    list_display = ('cve_titular', 'nom_titular')
    search_fields = ('nom_titular',)

@admin.register(Dependencia)
class DependenciaAdmin(admin.ModelAdmin):
    """Administrador para Dependencias"""
    list_display = ('cve_dep', 'nom_dep', 'old_titular', 'titular_fk') # Changed titular to old_titular and added titular_fk
    search_fields = ('nom_dep', 'old_titular', 'titular_fk__nom_titular') # Changed titular to old_titular and added titular_fk__nom_titular

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Administrador personalizado para CustomUser"""
    
    # Campos a mostrar en la lista
    list_display = ('username', 'nombre_completo', 'dependencia', 'tipo_usuario', 'is_active', 'date_joined')
    list_filter = ('tipo_usuario', 'is_active', 'genero', 'date_joined', 'dependencia')
    search_fields = ('username', 'nombre_completo', 'dependencia__nom_dep', 'email')
    
    # Campos en el formulario de edición
    fieldsets = UserAdmin.fieldsets + (
        ('Información de la Dependencia', {
            'fields': ('dependencia', 'direccion')
        }),
        ('Información Personal Adicional', {
            'fields': ('nombre_completo', 'genero', 'tipo_usuario')
        }),
    )
    
    # Campos al crear usuario nuevo
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Información Adicional', {
            'fields': ('nombre_completo', 'dependencia', 
                      'direccion', 'genero', 'tipo_usuario', 'email')
        }),
    )

@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    """Administrador para Eventos"""
    
    list_display = ('nombre_evento', 'dependencia', 'estado', 'fecha_hora_inicio', 'asistira_gobernador')
    list_filter = ('estado', 'asistira_gobernador', 'fecha_hora_inicio', 'usuario_creador__dependencia')
    search_fields = ('nombre_evento', 'lugar_evento', 'numero_documento', 'usuario_creador__dependencia__nom_dep')
    readonly_fields = ('titular', 'dependencia', 'fecha_creacion', 'fecha_actualizacion')
    
    fieldsets = (
        ('Información del Evento', {
            'fields': ('nombre_evento', 'lugar_evento', 'numero_documento', 'asistira_gobernador')
        }),
        ('Archivo y Estado', {
            'fields': ('archivo_pdf', 'estado')
        }),
        ('Fechas y Horarios', {
            'fields': ('fecha_hora_inicio', 'fecha_hora_fin')
        }),
        ('Información Automática', {
            'fields': ('usuario_creador', 'titular', 'dependencia', 'fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )

@admin.register(LogEventoEstado)
class LogEventoEstadoAdmin(admin.ModelAdmin):
    """Administrador para Logs de cambio de estado"""
    
    list_display = ('evento', 'estado_anterior', 'estado_nuevo', 'usuario_cambio', 'fecha_cambio', 'automatico')
    list_filter = ('estado_anterior', 'estado_nuevo', 'automatico', 'fecha_cambio')
    search_fields = ('evento__nombre_evento', 'comentario')
    readonly_fields = ('evento', 'estado_anterior', 'estado_nuevo', 'usuario_cambio', 'fecha_cambio', 'automatico')