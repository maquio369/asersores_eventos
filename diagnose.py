#!/usr/bin/env python
"""
Script de diagnóstico para el sistema de eventos gubernamentales
Ejecutar dentro del contenedor Docker para verificar configuración
"""
import os
import sys
import django
from django.conf import settings

def check_environment():
    """Verificar variables de entorno"""
    print("=== VARIABLES DE ENTORNO ===")
    env_vars = ['DEBUG', 'DB_NAME', 'DB_USER', 'DB_HOST', 'DB_PORT', 'SECRET_KEY']
    for var in env_vars:
        value = os.environ.get(var, 'NO DEFINIDA')
        if var == 'SECRET_KEY' and value != 'NO DEFINIDA':
            value = value[:10] + '...'  # Ocultar la clave
        print(f"{var}: {value}")
    print()

def check_database():
    """Verificar conexión a la base de datos"""
    print("=== CONEXIÓN A BASE DE DATOS ===")
    try:
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("SELECT version()")
        version = cursor.fetchone()[0]
        print(f"✅ Conexión exitosa - PostgreSQL: {version}")
        
        # Verificar tablas
        cursor.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public'")
        table_count = cursor.fetchone()[0]
        print(f"✅ Tablas en la base de datos: {table_count}")
        
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
    print()

def check_static_files():
    """Verificar archivos estáticos"""
    print("=== ARCHIVOS ESTÁTICOS ===")
    static_root = getattr(settings, 'STATIC_ROOT', None)
    if static_root and os.path.exists(static_root):
        file_count = sum([len(files) for r, d, files in os.walk(static_root)])
        print(f"✅ STATIC_ROOT existe: {static_root}")
        print(f"✅ Archivos estáticos: {file_count}")
    else:
        print(f"❌ STATIC_ROOT no existe o no configurado: {static_root}")
    print()

def check_media_files():
    """Verificar directorio de media"""
    print("=== ARCHIVOS MEDIA ===")
    media_root = getattr(settings, 'MEDIA_ROOT', None)
    if media_root and os.path.exists(media_root):
        print(f"✅ MEDIA_ROOT existe: {media_root}")
    else:
        print(f"❌ MEDIA_ROOT no existe: {media_root}")
    print()

def check_apps():
    """Verificar aplicaciones instaladas"""
    print("=== APLICACIONES INSTALADAS ===")
    for app in settings.INSTALLED_APPS:
        print(f"- {app}")
    print()

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eventos_gubernamentales.settings_docker')
    
    try:
        django.setup()
        print("🔍 DIAGNÓSTICO DEL SISTEMA DE EVENTOS GUBERNAMENTALES")
        print("=" * 60)
        
        check_environment()
        check_database()
        check_static_files()
        check_media_files()
        check_apps()
        
        print("✅ Diagnóstico completado")
        
    except Exception as e:
        print(f"❌ Error durante el diagnóstico: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()