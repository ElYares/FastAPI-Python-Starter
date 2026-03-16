.PHONY: install install-dev run test test-docker lint format security check migrate up down logs

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

security:
	bandit -q -c bandit.yaml -r app
	pip-audit -r requirements/base.txt --no-deps --disable-pip

check: lint test security

migrate:
	docker compose exec fastapi alembic upgrade head

up:
	docker compose up --build -d

down:
	docker compose down

logs:
	docker compose logs -f fastapi
