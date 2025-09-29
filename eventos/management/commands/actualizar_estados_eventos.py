
import logging
from django.core.management.base import BaseCommand
from django.utils import timezone
from eventos.models import Evento, LogEventoEstado

# Configurar un logger para este comando
logger = logging.getLogger(__name__)

class Command(BaseCommand):
    """
    Comando de Django para actualizar automáticamente los estados de los eventos.
    - Cambia eventos de 'programado' a 'activo' si la hora de inicio ya pasó.
    - Cambia eventos de 'activo' o 'programado' a 'finalizado' si la hora de fin ya pasó.
    """
    help = 'Actualiza los estados de los eventos según la fecha y hora actual.'

    def handle(self, *args, **options):
        """
        Lógica principal del comando.
        """
        ahora = timezone.now()
        self.stdout.write(f"[{ahora.strftime('%Y-%m-%d %H:%M:%S')}] Iniciando la actualización de estados de eventos...")

        # 1. Transición de 'Programado' a 'Activo'
        # Busca eventos programados cuya fecha de inicio ya pasó pero cuya fecha de fin aún no.
        eventos_para_activar = Evento.objects.filter(
            estado='programado',
            fecha_hora_inicio__lte=ahora,
            fecha_hora_fin__gt=ahora
        )
        
        count_activados = 0
        for evento in eventos_para_activar:
            estado_anterior = evento.estado
            evento.estado = 'activo'
            evento.save()
            
            # Registrar en el log
            LogEventoEstado.objects.create(
                evento=evento,
                estado_anterior=estado_anterior,
                estado_nuevo='activo',
                comentario='El evento ha iniciado.',
                automatico=True
            )
            count_activados += 1
        
        if count_activados > 0:
            self.stdout.write(self.style.SUCCESS(f"  -> {count_activados} evento(s) pasaron a estado 'Activo'."))

        # 2. Transición a 'Finalizado'
        # Busca eventos programados o activos cuya fecha de finalización ya pasó.
        eventos_para_finalizar = Evento.objects.filter(
            estado__in=['programado', 'activo'],
            fecha_hora_fin__lte=ahora
        )
        
        count_finalizados = 0
        for evento in eventos_para_finalizar:
            estado_anterior = evento.estado
            evento.estado = 'finalizado'
            evento.save()
            
            # Registrar en el log
            LogEventoEstado.objects.create(
                evento=evento,
                estado_anterior=estado_anterior,
                estado_nuevo='finalizado',
                comentario='El evento ha concluido.',
                automatico=True
            )
            count_finalizados += 1

        if count_finalizados > 0:
            self.stdout.write(self.style.SUCCESS(f"  -> {count_finalizados} evento(s) pasaron a estado 'Finalizado'."))

        total_cambios = count_activados + count_finalizados
        if total_cambios == 0:
            self.stdout.write(self.style.NOTICE("  No hubo cambios de estado en esta ejecución."))
        
        self.stdout.write(f"[{timezone.now().strftime('%Y-%m-%d %H:%M:%S')}] Proceso de actualización finalizado.")

