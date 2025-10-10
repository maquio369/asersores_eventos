#!/bin/bash
echo "Reconstruyendo contenedor..."
docker-compose down
docker system prune -f
docker-compose build --no-cache
docker-compose up -d
echo "Contenedor reconstruido. Verificando logs..."
sleep 5
docker-compose logs web