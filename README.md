# Sistema de Gestión de Eventos Gubernamentales

Una aplicación web desarrollada con Django para la gestión, seguimiento y calendarización de eventos gubernamentales. Permite a diferentes dependencias registrar sus eventos y a los administradores supervisarlos y gestionarlos de forma centralizada.

## ✨ Características Principales

- **Gestión de Usuarios:** Roles de `Administrador` y `Usuario de Captura` con diferentes permisos.
- **CRUD de Eventos:** Creación, lectura, actualización y cancelación de eventos.
- **Dashboard Interactivo:** Visualización rápida de estadísticas de eventos (totales, programados, finalizados) y filtros dinámicos por período (día, semana, mes).
- **Calendario de Eventos:** Vista de calendario mensual para una mejor planificación.
- **Notificaciones por Correo:** Envío automático de correos al crear o actualizar un evento.
- **Actualización Automática de Estados:** Un comando de gestión (`actualizar_estados_eventos`) cambia el estado de los eventos de `Programado` a `Activo` y a `Finalizado` según la hora.
- **Filtros Avanzados:** Búsqueda por texto, estado, municipio, dependencia y fechas.
- **Seguridad:** Uso de variables de entorno para proteger información sensible.

## 🛠️ Tecnologías Utilizadas

- **Backend:** Django, Django REST Framework
- **Base de Datos:** PostgreSQL
- **Frontend:** HTML, CSS, JavaScript, Bootstrap 5
- **Librerías Python:** `psycopg2-binary`, `python-decouple`, `django-bootstrap5`, `reportlab`.

---

## 🚀 Puesta en Marcha (Desarrollo Local)

Sigue estos pasos para configurar el entorno de desarrollo en tu máquina local.

### 1. Prerrequisitos

- **Python 3.8+**
- **PostgreSQL:** Un servidor de base de datos PostgreSQL instalado y en ejecución.
- **Git**

### 2. Clonar el Repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd sistema_eventos_gubernamentales
```

### 3. Configurar el Entorno Virtual

Es una buena práctica aislar las dependencias del proyecto.

```bash
# Crear el entorno virtual
python -m venv venv

# Activar el entorno
# En Windows:
venv\Scripts\activate
# En macOS/Linux:
source venv/bin/activate
```

### 4. Instalar Dependencias

Instala todas las librerías de Python necesarias con un solo comando.

```bash
pip install -r requirements.txt
```

### 5. Configurar la Base de Datos

1.  Abre tu cliente de PostgreSQL (como `psql` o pgAdmin).
2.  Crea una nueva base de datos para el proyecto. Por ejemplo: `eventos_db`.
3.  Asegúrate de tener un usuario y contraseña con permisos sobre esa base de datos.

### 6. Configurar Variables de Entorno

Este proyecto utiliza un archivo `.env` para gestionar la configuración sensible.

1.  Crea una copia del archivo de ejemplo:
    ```bash
    # En Windows (Command Prompt)
    copy .env.example .env
    # En Windows (PowerShell)
    cp .env.example .env
    # En macOS/Linux
    cp .env.example .env
    ```
2.  Abre el nuevo archivo `.env` y edita las variables con tus propios valores, especialmente la configuración de la base de datos (`DB_...`) y del correo (`EMAIL_...`).

### 7. Aplicar Migraciones

Este comando creará las tablas necesarias en tu base de datos.

```bash
python manage.py migrate
```

### 8. Crear un Superusuario

Necesitarás un usuario administrador para acceder al panel de Django y gestionar la aplicación.

```bash
python manage.py createsuperuser
```
Sigue las instrucciones en la terminal para crear tu usuario. **Importante:** Al crear el usuario, asegúrate de asignarle el `tipo_usuario` como `admin` a través del shell de Django o el panel de administración para tener todos los permisos.

### 9. Ejecutar el Servidor de Desarrollo

¡Todo listo! Inicia el servidor.

```bash
python manage.py runserver
```

La aplicación estará disponible en `http://127.0.0.1:8000/`.

---

## ⚙️ Comandos de Gestión

### Actualizar Estados de Eventos

Este comando es crucial para que el sistema funcione correctamente. Debe ejecutarse periódicamente (por ejemplo, cada 5-10 minutos) en un entorno de producción.

```bash
python manage.py actualizar_estados_eventos
```

En producción, esto se configura normalmente con un **cron job** (en Linux) o una Tarea Programada (en Windows).