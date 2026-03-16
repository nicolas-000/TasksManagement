# Task Manager API

Servicio backend para gestionar tareas de un equipo, desarrollado con Django y Django REST Framework.

## Requisitos previos

- Python 3.11+
- Docker (opcional)

## Ejecución local

```bash
# Instalar dependencias
pip install -r requirements.txt

# Aplicar migraciones
python manage.py migrate

# Iniciar el servidor
python manage.py runserver
```

El servicio estará disponible en `http://localhost:8000`.

## Ejecución con Docker

```bash
# Construir la imagen
docker build -t task-manager .

# Ejecutar el contenedor
docker run -p 8000:8000 task-manager
```

## Endpoints

| Método | Ruta | Autenticación | Descripción |
|--------|------|---------------|-------------|
| POST | `/signup/` | No | Registrar usuario |
| POST | `/signin/` | No | Iniciar sesión (devuelve tokens JWT) |
| GET | `/tasks/` | Bearer token | Listar tareas |
| POST | `/tasks/` | Bearer token | Crear tarea |
| GET | `/tasks/{id}/` | Bearer token | Detalle de una tarea |
| PATCH | `/tasks/{id}/` | Bearer token | Actualizar tarea |
| DELETE | `/tasks/{id}/` | Bearer token | Eliminar tarea |

### Ejemplo de uso

```bash
# Registrar usuario
curl -X POST http://localhost:8000/signup/ \
  -H "Content-Type: application/json" \
  -d '{"username": "usuario1", "email": "usuario1@mail.com", "password": "mipassword123"}'

# Iniciar sesión
curl -X POST http://localhost:8000/signin/ \
  -H "Content-Type: application/json" \
  -d '{"username": "usuario1", "password": "mipassword123"}'
# Respuesta: { "access": "<token>", "refresh": "<token>", "user": {...} }

# Crear tarea (usar el token de acceso)
curl -X POST http://localhost:8000/tasks/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"title": "Mi tarea", "description": "Descripción", "status": "pending"}'
```

### Filtros, paginación y ordenamiento en `/tasks/`

| Parámetro | Ejemplo | Descripción |
|-----------|---------|-------------|
| `status` | `?status=pending` | Filtrar por estado (`pending`, `in_progress`, `done`) |
| `created_by` | `?created_by=1` | Filtrar por ID del creador |
| `assigned_to` | `?assigned_to=2` | Filtrar por ID del asignado |
| `ordering` | `?ordering=title` | Ordenar por campo (`title`, `created_at`, `status`). Prefijo `-` para descendente |
| `page` | `?page=2` | Paginación (10 resultados por página) |

## Decisiones técnicas

- **Django + Django REST Framework**: Framework robusto con ORM integrado, sistema de autenticación nativo y amplio ecosistema. DRF facilita la serialización, validación y manejo de vistas genéricas para CRUD.

- **JWT con `djangorestframework-simplejwt`**: Autenticación stateless mediante tokens. El token de acceso expira en 1 hora y el de refresh en 7 días.

- **Modelo de usuario de Django (`auth.User`)**: Se reutiliza el modelo integrado de Django en lugar de crear uno personalizado, ya que cubre los campos necesarios (username, email, password hasheado).

- **SQLite**: Base de datos ligera que no requiere configuración externa. Adecuada para el alcance del proyecto y simplifica el despliegue.

- **`django-filter`**: Permite declarar filtros de forma limpia con `FilterSet`, evitando lógica manual de filtrado en las vistas.

- **Gunicorn en Docker**: Servidor WSGI de producción en lugar del servidor de desarrollo de Django. La imagen usa `python:3.13-slim` para mantener un tamaño reducido.

- **Separación en dos apps (`users` y `tasks`)**: Cada app maneja una responsabilidad distinta, facilitando el mantenimiento y la escalabilidad del proyecto.

- **Variables de entorno**: `SECRET_KEY`, `DEBUG` y `ALLOWED_HOSTS` se leen desde variables de entorno, permitiendo configuración segura en producción sin modificar el código.
