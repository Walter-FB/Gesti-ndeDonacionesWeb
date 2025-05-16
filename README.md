# Sistema de Gestión de Donaciones para Comedores Comunitarios

Este es un MVP (Producto Mínimo Viable) desarrollado con FastAPI que permite gestionar donaciones para comedores comunitarios.

## Funcionalidades

- Registro de comedores comunitarios (nombre, barrio, persona responsable, contacto)
- Registro de donaciones disponibles (tipo, cantidad, urgencia)
- Notificación automática a comedores cuando hay donaciones disponibles
- Endpoint para que los comedores respondan si aceptan la donación

## Requisitos

- Python 3.8+
- Dependencias listadas en `requirements.txt`

## Instalación

1. Clonar el repositorio:
```
git clone <url-del-repositorio>
cd <nombre-del-directorio>
```

2. Crear un entorno virtual e instalar las dependencias:
```
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Ejecución

Para ejecutar la aplicación:

```
python run.py
```

La aplicación estará disponible en `http://localhost:8000`

## Estructura del Proyecto

- `app/`: Directorio principal de la aplicación
  - `main.py`: Archivo principal con las rutas de FastAPI
  - `models.py`: Modelos de la base de datos
  - `schemas.py`: Esquemas de Pydantic
  - `database.py`: Configuración de la base de datos
  - `email_service.py`: Servicio simulado de envío de correos
  - `templates/`: Plantillas HTML
  - `static/`: Archivos estáticos (CSS, JS, imágenes)
- `requirements.txt`: Dependencias del proyecto
- `run.py`: Archivo para ejecutar la aplicación

## API Endpoints

### Comedores
- `GET /comedores`: Lista todos los comedores
- `GET /comedores/nuevo`: Formulario para registrar un nuevo comedor
- `POST /comedores/nuevo`: Registra un nuevo comedor
- `GET /comedores/{comedor_id}/notificaciones`: Muestra las notificaciones para un comedor

### Donaciones
- `GET /donaciones`: Lista todas las donaciones
- `GET /donaciones/nueva`: Formulario para registrar una nueva donación
- `POST /donaciones/nueva`: Registra una nueva donación

### API
- `POST /api/donaciones/{donacion_id}/aceptar/{comedor_id}`: Endpoint para que un comedor acepte una donación 