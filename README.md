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
