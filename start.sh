#!/bin/bash
set -e

# Verificar que las dependencias estén instaladas
echo "Verificando dependencias..."
python -c "import django; import bootstrap5; import openpyxl; print('Todas las dependencias OK')"

# Esperar a que la base de datos esté disponible
echo "Esperando a que la base de datos esté disponible..."
while ! nc -z $DB_HOST $DB_PORT; do
  sleep 1
done
echo "Base de datos disponible!"

# Configurar Django settings
export DJANGO_SETTINGS_MODULE=eventos_gubernamentales.settings_docker

# Ejecutar migraciones
echo "Ejecutando migraciones..."
python manage.py migrate

# Recopilar archivos estáticos
echo "Recopilando archivos estáticos..."
python manage.py collectstatic --noinput

# Iniciar servidor Django
echo "Iniciando servidor..."
python manage.py runserver 0.0.0.0:8000