# FastAPI Starter - Agent Guidelines

This document provides comprehensive guidelines for agentic coding agents working in this FastAPI Python Starter repository.

## Build/Lint/Test Commands

### Running Tests
```bash
# Run all tests (Docker)
docker compose exec fastapi pytest -q

# Run all tests (verbose)
docker compose exec fastapi pytest -vv

# Run single test file
docker compose exec fastapi pytest -q tests/test_auth.py
docker compose exec fastapi pytest -q tests/test_users.py
docker compose exec fastapi pytest -q tests/test_exceptions.py

# Run tests locally
pytest -q
pytest tests/test_auth.py
```

### Code Formatting
```bash
# Format code with Black
black .

# Check formatting without modifying
black --check .
```

### Development Server
```bash
# Local development
uvicorn app.main:app --reload

# Docker development
docker compose up --build -d
docker compose logs -f fastapi
```

### Database Migrations
```bash
# Apply migrations
docker compose exec fastapi alembic upgrade head

# Create new migration
docker compose exec fastapi alembic revision --autogenerate -m "description"
```

## Code Style Guidelines

### Import Organization
- Use `from __future__ import annotations` at the top of all Python files
- Imports should be organized in this order:
  1. Standard library imports
  2. Third-party imports (FastAPI, SQLAlchemy, etc.)
  3. Local application imports (from app.*)
- Use absolute imports for local modules (e.g., `from app.config import settings`)

### Type Hints
- All functions must have type hints for parameters and return values
- Use union types with `|` syntax (Python 3.10+) instead of `Union`
- Use `EmailStr` from Pydantic for email fields
- Always type database session parameters as `Session` from SQLAlchemy

### Class and Function Conventions
- Use PascalCase for class names (e.g., `AuthService`, `UserRepository`)
- Use snake_case for function and variable names
- Service classes should follow the pattern: `[Name]Service`
- Repository classes should follow the pattern: `[Name]Repository`
- Schema files should use descriptive names like `UserResponse`, `TokenResponse`

### API Route Structure
- Use FastAPI's `APIRouter` with appropriate tags
- Include comprehensive docstrings with `summary`, `description`, and detailed parameter documentation
- Return properly typed response models using Pydantic schemas
- Use dependency injection for database sessions and authentication
- Apply OAuth2PasswordRequestForm for authentication endpoints

### Error Handling
- Use custom exceptions from `app.exceptions`: `NotFoundException`, `BadRequestException`
- Return consistent error response format: `{"error": "message"}`
- Handle validation errors through Pydantic automatically
- Use HTTP status codes appropriately (404, 400, 401, 500)

### Database and Models
- Use SQLAlchemy 2.0+ with async support where applicable
- Define Pydantic schemas in `app/shemas/` directory (note: "shemas" not "schemas")
- Use `from_attributes = True` in Pydantic Config for ORM models
- Separate domain models in `app/models/` from database models
- Use repository pattern for data access

### Authentication and Security
- Use JWT tokens with `python-jose` library
- Hash passwords with bcrypt via `passlib` (72-byte limit)
- Use `OAuth2PasswordRequestForm` for Swagger compatibility
- Include proper token expiration validation
- Store JWT settings in configuration (secret key, algorithm, expiration)

### Configuration Management
- Use `pydantic-settings` with BaseSettings for configuration
- Load environment variables from `.env` file
- Use type hints for all configuration fields
- Include sensible defaults for development
- Separate database URL, JWT settings, and CORS origins in config

### Logging and Documentation
- Use structured logging with appropriate log levels
- Include request/response logging for debugging
- Document all public API endpoints with Swagger/OpenAPI tags
- Use descriptive variable names and inline comments where logic is complex

### Testing Standards
- Use pytest for all tests
- Test both success and error paths
- Use TestClient for API endpoint testing
- Mock external dependencies where appropriate
- Include tests for authentication flows and token validation
- Test exception handlers and error responses

### File Organization
```
app/
├── api/v1/           # API route definitions by version
├── dependencies/     # FastAPI dependencies (auth, db)
├── models/          # Domain and database models
├── repositories/    # Data access layer
├── service/         # Business logic layer
├── shemas/          # Pydantic schemas (note spelling)
├── config.py        # Application settings
├── exceptions.py    # Custom exceptions
├── logger.py        # Logging configuration
├── main.py         # FastAPI app entry point
└── middleware.py   # Global middleware setup
```

### Security Best Practices
- Never log or expose sensitive data (passwords, tokens)
- Validate all input data using Pydantic schemas
- Use HTTPS in production
- Implement proper CORS configuration
- Rate limit authentication endpoints
- Use environment variables for secrets

This codebase follows clean architecture principles with clear separation between API, business logic, and data access layers. All new code should maintain these patterns and conventions.