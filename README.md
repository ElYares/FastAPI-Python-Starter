# FASTAPI Python Starter

Proyecto base para crear APIs modernas con **FastAPI** siguiendo buenas practicas de arquitectura mediante el patron `Repository + Service`. Ideal para construir microservicios limpios, escalables y faciles de mantener.


---

## Caracteristicas

- Estructura modular con separación por capas  
- Uso del patrón Repository + Service  
- Tipado fuerte con Pydantic  
- Configuración vía `.env`  
- Dockerfile listo para desarrollo local  
- Ejemplos de rutas básicas (GET, POST)  
- Preparado para pruebas unitarias  

---

## Estructura del Proyecto
<pre>
app/
├── api
│   └── v1
│       ├── auth_routes.py        # Rutas para autenticación: /login
│       ├── health_routes.py      # Ruta de verificación de estado: /health
│       ├── routes.py             # Rutas generales, en este caso para /users
│       └── secure_routes.py      # Rutas protegidas por JWT: /secure
├── config.py                     # Configuración global del proyecto vía .env usando Pydantic
├── dependencies
│   └── auth.py                   # Dependencias reutilizables
├── exceptions.py                 # Manejo de errores personalizados (si no lo tienes, te lo puedo generar)
├── logger.py                     # Configuración del sistema de logging (nivel, formato, salida)
├── main.py                       # Punto de entrada de la app FastAPI, incluye rutas y metadatos
├── middleware.py                 # Middleware para procesamiento de peticiones/respuestas
├── models
│   └── user.py                   # Modelo de dominio: User (desacoplado de Pydantic)
├── repositories
│   └── user_repository.py        # Lógica de acceso a datos
├── service
│   ├── auth_service.py           # Lógica de negocio relacionada con JWT: creación y validación
│   └── user_service.py           # Lógica de negocio para usuarios, usa UserRepository
└── shemas
    └── user_shema.py             # Esquemas Pydantic para entrada/salida de datos HTTP

tests/
├── test_auth.py                  # Prueba de flujo completo de login y acceso protegido
└── test_users.py                 # Prueba para listar usuarios

pytest.ini                        # Configuración de pytest para testeo automatizado
requirements.txt                 # Lista de dependencias necesarias
README.md                         # Documentación del proyecto
LICENSE                           # Licencia del proyecto

</pre>
---

### Requisitos
- Python 3.11+
- Docker (opcional pero recomendado)

## Flujo de ramas y versiones


Este repositorio sigue una convención simple para manejar versiones de desarrollo y producción:

| Rama        | Propósito                                 |
|-------------|-------------------------------------------|
| `main`      | Rama estable para producción               |
| `dev-v1`    | Rama activa de desarrollo para la versión 1 |
| `feature/*` | Funcionalidades nuevas en progreso         |
| `hotfix/*`  | Correcciones urgentes directamente en producción |

---


### Flujo de trabajo

1. Todas las funcionalidades nuevas deben crearse en ramas `feature/*`, por ejemplo:
   ```bash
   git checkout -b feature/crear-endpoint-usuarios



### Uso con Docker
```bash
docker-compose up --build -d && docker-compose logs -f && docker-compose down
```

### Test Con Docker
```bash
docker compose exec fastapi pytest
```

### Local Sin Docker
```bash
python -m venv venv
```

```bash
source venv/bin/activate
```


```bash
pip install -r requirements.txt
```


```bash
uvicorn app.main:app --reload
```




