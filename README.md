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
├── app
│   ├── api
│   │   └── v1
│   │       └── routes.py
│   ├── config.py
│   ├── main.py
│   ├── models
│   │   ├── __pycache__
│   │   │   └── user.cpython-313.pyc
│   │   └── user.py
│   ├── __pycache__
│   │   └── main.cpython-313.pyc
│   ├── repositories
│   │   ├── __pycache__
│   │   │   └── user_repository.cpython-313.pyc
│   │   └── user_repository.py
│   ├── service
│   │   ├── __pycache__
│   │   │   └── user_service.cpython-313.pyc
│   │   └── user_service.py
│   └── shemas
│       ├── __pycache__
│       │   └── user_shema.cpython-313.pyc
│       └── user_shema.py
├── LICENSE
├── README.md
├── requirements.txt
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
