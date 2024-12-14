.PHONY: build up down test logs clean help prod-build prod-up prod-down prod-logs dev debug migrate-up migrate-down migrate-create

help:
	@echo "Available commands:"
	@echo "Development:"
	@echo "  build   - Build all docker containers"
	@echo "  up      - Start all containers in detached mode"
	@echo "  down    - Stop all containers"
	@echo "  test    - Run tests in container"
	@echo "  logs    - View container logs"
	@echo "  clean   - Stop and remove all containers, volumes, and orphans"
	@echo "  dev     - Build, run, and show logs for development"
	@echo "  debug   - Show status and logs of all containers"
	@echo "Production:"
	@echo "  prod-build - Build production docker containers"
	@echo "  prod-up    - Start production containers in detached mode"
	@echo "  prod-down  - Stop production containers"
	@echo "  prod-logs  - View production container logs"
	@echo "  help    - Show this help message"
	@echo "Database:"
	@echo "  migrate-up - Upgrade database to the latest revision"
	@echo "  migrate-down - Downgrade database to the previous revision"
	@echo "  migrate-create - Create a new migration"

build:
	docker compose build

up:
	docker compose up -d

down:
	docker compose down

test:
	docker compose up -d api
	docker compose logs api
	docker compose run --service-ports -e PYTHONPATH=/app test pytest tests/ -v --color=yes

logs:
	docker compose logs -f

clean:
	docker compose down -v --remove-orphans

prod-build:
	docker compose -f compose.prod.yml build

prod-up:
	docker compose -f compose.prod.yml up -d

prod-down:
	docker compose -f compose.prod.yml down

prod-logs:
	docker compose -f compose.prod.yml logs -f

dev:
	docker compose down || true
	docker compose build --progress=plain && docker compose up

debug:
	@echo "=== Container Status ==="
	docker compose ps
	@echo "\n=== Container Logs ==="
	docker compose logs
	@echo "\n=== Health Check Status ==="
	docker compose ps api --format "{{.Status}}"

migrate-up:
	alembic upgrade head

migrate-down:
	alembic downgrade -1

migrate-create:
	alembic revision -m "$(name)"
