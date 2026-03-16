# FASTAPI Python Starter

Proyecto base para crear APIs modernas con **FastAPI** siguiendo buenas prácticas de arquitectura mediante el patrón **Repository + Service**.  
Incluye **JWT (Bearer)**, **Swagger listo para probar**, **CORS configurable por `.env`**, **Docker Compose** y **tests**.

---

## Características

- Estructura modular con separación por capas
- Patrón **Repository + Service**
- Tipado fuerte con **Pydantic**
- Configuración vía `.env` con **pydantic-settings**
- **JWT Bearer** (login + rutas protegidas)
- **Swagger (/docs)** con autorización por **Bearer token** (pegar token y listo)
- **CORS** configurable por variable `ALLOWED_ORIGINS`
- Logging centralizado
- Manejo de errores consistente (handlers) + endpoints de prueba para tests
- Docker Compose con:
  - `env_file`
  - `healthcheck`
  - red dedicada `fast-starter-api`
- Pruebas automáticas con `pytest`

---

## Documentación (Swagger / OpenAPI)

FastAPI genera la documentación automáticamente al ejecutar la app:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- OpenAPI JSON: `http://localhost:8000/openapi.json`

### Probar Auth en Swagger

1. Ejecuta `POST /api/v1/login` para obtener el token:
   ```json
   {
     "access_token": "…",
     "token_type": "bearer"
   }
   ```
2. Click en **Authorize** y pega el `access_token` (solo el token).
3. Prueba `GET /api/v1/secure`.

---

## Estructura del Proyecto

> Nota: el directorio se llama `shemas/` (manteniendo tu estructura actual).

<pre>
elyares-fastapi-python-starter/
├── README.md
├── docker-compose.yaml
├── Dockerfile
├── LICENSE
├── pytest.ini
├── requirements.txt
├── app/
│   ├── config.py                    # Settings (.env) con pydantic-settings
│   ├── exceptions.py                # Excepciones custom (NotFound/BadRequest)
│   ├── logger.py                    # Logger global
│   ├── main.py                      # Entry-point: incluye routers, middlewares, handlers
│   ├── middleware.py                # setup_middlewares(app) + CORS configurable
│   ├── api/
│   │   └── v1/
│   │       ├── auth_routes.py       # POST /login (JWT)
│   │       ├── health_routes.py     # GET /health
│   │       ├── routes.py            # GET /users
│   │       └── secure_routes.py     # GET /secure (protegido)
│   ├── dependencies/
│   │   └── auth.py                  # Validación JWT + esquema Bearer para Swagger
│   ├── models/
│   │   └── user.py                  # Modelo de dominio (desacoplado)
│   ├── repositories/
│   │   └── user_repository.py       # Acceso a datos (mock/in-memory)
│   ├── service/
│   │   ├── auth_service.py          # Creación de JWT (exp, sub)
│   │   └── user_service.py          # Casos de uso de usuarios
│   └── shemas/
│       └── user_shema.py            # Schemas Pydantic (UserResponse, TokenResponse, etc.)
└── tests/
    ├── test_auth.py                 # Tests de login + /secure (JWT)
    ├── test_exceptions.py           # Tests de errores (404/400/500)
    └── test_users.py                # Tests para /users
</pre>

---

## Requisitos

- Python 3.11+
- Docker (opcional pero recomendado)
- Make (opcional, para atajos de comandos)


---

## Uso con Docker (recomendado)

### Levantar API
```bash
docker compose up --build -d
```

### Logs
```bash
docker compose logs -f fastapi
```

### Bajar
```bash
docker compose down
```

### Red dedicada
Este starter usa una red bridge llamada:
- `fast-starter-api`

Puedes verificar:
```bash
docker network ls | grep fast-starter-api
```

---

## Ejecución local (sin Docker)

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements/base.txt -r requirements/dev.txt -r requirements/test.txt
uvicorn app.main:app --reload
```

O con Make:
```bash
make install-dev
make run
```

---

## Endpoints principales

- `GET  /api/v1/health` → estado del servicio
- `POST /api/v1/login` → genera `access_token`
- `POST /api/v1/refresh` → rota `refresh_token` y devuelve nuevo par de tokens
- `GET  /api/v1/users` → lista usuarios (demo)
- `GET  /api/v1/secure` → protegido por JWT (Bearer)

### Endpoints de soporte para tests de exceptions
- `GET /api/v1/not-found` → retorna 404 con `{"error": "..."}`
- `GET /api/v1/bad-request` → retorna 400 con `{"error": "..."}`
- `GET /api/v1/exception` → retorna 500 con `{"error": "Internal Server Error"}`

> Recomendación: si quieres, estos endpoints se pueden habilitar **solo en development** usando `APP_ENV`.

---

## Probar CORS (Postman / Yak)

### Origin permitido (debe regresar `access-control-allow-origin`)
- `GET /api/v1/health` con header:
  - `Origin: http://localhost:5173`

### Origin NO permitido (preflight debe fallar)
- `OPTIONS /api/v1/secure`
  - `Origin: http://evil.com`
  - `Access-Control-Request-Method: GET`

---

## Tests

### Con Docker
```bash
docker compose exec fastapi pytest -q
```

Más verbose:
```bash
docker compose exec fastapi pytest -vv
```

### Por archivo
```bash
docker compose exec fastapi pytest -q tests/test_auth.py
```

### Local
```bash
make test
```

## Calidad de código

Lint/format:
```bash
make lint
make format
```

Pre-commit:
```bash
pre-commit install
pre-commit run --all-files
```

---

## Flujo de ramas y versiones (sugerido)

| Rama         | Propósito |
|--------------|-----------|
| `main`       | Rama estable / producción |
| `dev-v1`     | Desarrollo activo |
| `feature/*`  | Funcionalidades nuevas |
| `hotfix/*`   | Correcciones urgentes |

Ejemplo:
```bash
git checkout -b feature/nueva-funcionalidad
```

---

## Migraciones

### Con Docker
```bash
docker compose exec fastapi alembic upgrade head
```

### Por archivo
```bash
docker compose exec fastapi alembic upgrade head
```

### Crear migración (autogenerate)
```bash
docker compose exec fastapi alembic revision --autogenerate -m "create users table"
```
---

## Roadmap (próximas épicas sugeridas)

- **ÉPICA 3 (opcional hardening):** endpoints de exceptions solo en `development`
- **ÉPICA 5:** Persistencia (DB) + registro/login real (usuarios en DB)
- **ÉPICA 6:** Observabilidad (request-id, logging JSON, readiness/liveness)
- **ÉPICA 7:** CI/CD (lint + tests + build)
