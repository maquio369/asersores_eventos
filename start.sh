#!/bin/bash

# Esperar a que la base de datos esté disponible
echo "Esperando a que la base de datos esté disponible..."
while ! nc -z $DB_HOST $DB_PORT; do
  sleep 1
done
echo "Base de datos disponible!"

# Ejecutar migraciones
echo "Ejecutando migraciones..."
python manage.py migrate --settings=eventos_gubernamentales.settings_docker

# Recopilar archivos estáticos
echo "Recopilando archivos estáticos..."
python manage.py collectstatic --noinput --settings=eventos_gubernamentales.settings_docker

# Iniciar servidor Django con gunicorn
echo "Iniciando servidor con gunicorn..."
gunicorn eventos_gubernamentales.wsgi_docker:application --bind 0.0.0.0:8000 --workers 3 --timeout 120