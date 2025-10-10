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

# Iniciar servidor Django
echo "Iniciando servidor..."
python manage.py runserver 0.0.0.0:8000 --settings=eventos_gubernamentales.settings_docker