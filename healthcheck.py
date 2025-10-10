#!/usr/bin/env python
import os
import sys
import django
from django.conf import settings
from django.core.management import execute_from_command_line

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eventos_gubernamentales.settings_docker')
    try:
        django.setup()
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        print("Database connection: OK")
        sys.exit(0)
    except Exception as e:
        print(f"Health check failed: {e}")
        sys.exit(1)