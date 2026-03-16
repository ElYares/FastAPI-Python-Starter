.PHONY: install install-dev run test test-docker lint format check migrate up down logs

install:
	pip install -r requirements/base.txt

install-dev:
	pip install -r requirements/base.txt -r requirements/dev.txt -r requirements/test.txt

run:
	uvicorn app.main:app --reload

test:
	pytest -q

test-docker:
	docker compose exec fastapi pytest -q

lint:
	ruff check .
	black --check .

format:
	ruff check . --fix
	black .

check: lint test

migrate:
	docker compose exec fastapi alembic upgrade head

up:
	docker compose up --build -d

down:
	docker compose down

logs:
	docker compose logs -f fastapi
