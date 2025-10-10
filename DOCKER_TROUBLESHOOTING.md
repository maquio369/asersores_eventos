# Guía de Troubleshooting para Docker

## Problemas Comunes y Soluciones

### 1. Error 500 en /eventos/crear/

**Causa más común:** Configuración incorrecta o dependencias faltantes.

**Soluciones:**

1. **Verificar logs del contenedor:**
```bash
docker logs <container_name>
```

2. **Ejecutar diagnóstico dentro del contenedor:**
```bash
docker exec -it <container_name> python diagnose.py
```

3. **Verificar que bootstrap5 esté habilitado:**
   - El archivo `settings_docker.py` debe incluir `'bootstrap5'` en `INSTALLED_APPS`

### 2. Problemas de Base de Datos

**Verificar conexión:**
```bash
docker exec -it <container_name> python healthcheck.py
```

**Ejecutar migraciones manualmente:**
```bash
docker exec -it <container_name> python manage.py migrate --settings=eventos_gubernamentales.settings_docker
```

### 3. Problemas con Archivos Estáticos

**Recopilar archivos estáticos:**
```bash
docker exec -it <container_name> python manage.py collectstatic --noinput --settings=eventos_gubernamentales.settings_docker
```

### 4. Verificar Variables de Entorno

**Listar variables dentro del contenedor:**
```bash
docker exec -it <container_name> env | grep -E "(DB_|EMAIL_|DEBUG|SECRET_KEY)"
```

### 5. Reconstruir Contenedor

Si persisten los problemas:

1. **Detener y eliminar contenedor:**
```bash
docker-compose down
docker system prune -f
```

2. **Reconstruir imagen:**
```bash
docker-compose build --no-cache
```

3. **Iniciar nuevamente:**
```bash
docker-compose up -d
```

### 6. Comandos Útiles de Diagnóstico

**Acceder al shell del contenedor:**
```bash
docker exec -it <container_name> /bin/bash
```

**Ver logs en tiempo real:**
```bash
docker logs -f <container_name>
```

**Verificar estado del contenedor:**
```bash
docker ps
docker inspect <container_name>
```

### 7. Verificar Configuración de Red

**Verificar que el puerto esté expuesto:**
```bash
docker port <container_name>
```

**Probar conectividad:**
```bash
curl http://172.16.35.75:3020/
```

## Archivos Importantes

- `settings_docker.py` - Configuración específica para Docker
- `wsgi_docker.py` - WSGI para producción
- `start.sh` - Script de inicio del contenedor
- `diagnose.py` - Script de diagnóstico
- `healthcheck.py` - Verificación de salud del contenedor

## Contacto

Si los problemas persisten, revisar los logs detallados y verificar la configuración de red y base de datos.