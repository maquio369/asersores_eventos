# Usar Python 3.12 como imagen base
FROM python:3.12-slim

# Establecer variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Establecer directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    postgresql-client \
    netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements y instalar dependencias Python
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Verificar que django-bootstrap5 se instaló
RUN python -c "import bootstrap5; print('django-bootstrap5 instalado correctamente')"

# Copiar el proyecto
COPY . /app/

# Dar permisos al script de inicio
RUN chmod +x /app/start.sh

# Crear directorio para archivos estáticos y media
RUN mkdir -p /app/staticfiles /app/media

# Exponer puerto
EXPOSE 8000

# Comando por defecto
CMD ["/app/start.sh"]