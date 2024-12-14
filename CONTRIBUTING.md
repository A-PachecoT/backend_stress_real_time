# Developer Guide - StressMinder API

## Development Setup

### Prerequisites
- Python 3.11+
- Poetry (Python package manager)
- Docker and Docker Compose
- Git

### Initial Setup

1. Clone the repository:
```bash
git clone https://github.com/A-PachecoT/stressminder-api
cd stressminder-api
```

2. Install dependencies with Poetry:
```bash
poetry install
```

3. Set up pre-commit hooks:
```bash
poetry run pre-commit install
```

### Environment Setup

1. Create a `.env` file in the project root:
```bash
cp .env.example .env
```

2. Configure your environment variables in `.env`:
```env
# Development Settings
ENVIRONMENT=development
DEBUG=true

# Database
DATABASE_URL=mysql://user:password@localhost:3306/almacenamiento
DB_USER=user
DB_PASSWORD=password
DB_ROOT_PASSWORD=rootpassword

# Security
SECRET_KEY=your-secret-key-here
```

## Development Workflow

### Running the Application

1. Using Docker (recommended):
```bash
make dev
```

2. Without Docker (local development):
```bash
poetry run uvicorn app.main:app --reload
```

### Code Quality Tools

- **Formatting**: We use `black` and `isort`
```bash
poetry run black .
poetry run isort .
```

- **Linting**: We use `flake8`
```bash
poetry run flake8
```

### Running Tests

```bash
poetry run pytest
```

With coverage report:
```bash
poetry run pytest --cov=app --cov-report=html
```

## Docker Commands

### Development Environment
```bash
# Build containers
make build

# Start services
make up

# View logs
make logs

# Stop services
make down
```

### Production Environment
```bash
# Build production containers
make prod-build

# Start production services
make prod-up

# View production logs
make prod-logs

# Stop production services
make prod-down
```

## API Documentation

Once the application is running:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Database Migrations

We use Alembic for database migrations:

```bash
# Create a new migration
poetry run alembic revision --autogenerate -m "description"

# Run migrations
poetry run alembic upgrade head

# Rollback one version
poetry run alembic downgrade -1
```

## Commit Guidelines

We follow conventional commits specification:

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

Example:
```bash
git commit -m "feat(auth): add JWT authentication"
```

## Project Structure

```
stressminder-api/
├── app/
│   ├── api/
│   │   ├── endpoints/
│   │   │   ├── auth.py
│   │   │   ├── questions.py
│   │   │   ├── sensors.py
│   │   │   └── results.py
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py
│   │   └── calculations.py
│   ├── models/
│   ├── schemas/
│   └── services/
├── tests/
├── docker/
├── .env.example
├── docker-compose.yml
├── compose.prod.yml
├── Dockerfile
├── Makefile
└── pyproject.toml
```

## Getting Help

- Check the [FAQ](./docs/FAQ.md)
- Open an issue
- Contact the maintainers

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 