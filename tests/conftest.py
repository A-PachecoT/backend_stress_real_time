from typing import AsyncGenerator, Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from app.core.config import Settings, get_settings
from app.core.database import Base, get_db
from app.main import app
from app.models.sensor import Sensor  # Import models to ensure they're registered


class TestSettings(Settings):
    # Override all database settings for testing
    DB_HOST: str = ""
    DB_USER: str = ""
    DB_PASSWORD: str = ""
    DB_NAME: str = ""
    DB_PORT: int = 0

    @property
    def ASYNC_DATABASE_URL(self) -> str:
        return "sqlite+aiosqlite:///:memory:"

    class Config:
        case_sensitive = True


# Create test settings instance
test_settings = TestSettings()


# Override settings before any database operations
def get_test_settings():
    return test_settings


app.dependency_overrides[get_settings] = get_test_settings

# Create test engine with SQLite
test_engine = create_async_engine(
    test_settings.ASYNC_DATABASE_URL,
    poolclass=NullPool,
    connect_args={"check_same_thread": False},  # Needed for SQLite
)

TestingSessionLocal = sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture
async def db() -> AsyncGenerator:
    # Create all tables
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    # Create session
    async with TestingSessionLocal() as session:
        yield session

    # Clean up
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
def client(db: AsyncSession) -> Generator:
    async def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
    # Restore original settings after test
    app.dependency_overrides[get_settings] = get_test_settings


@pytest.fixture
def test_sensor_data():
    return {"temperatura": 36.5, "ritmo_cardiaco": 85}


@pytest.fixture
def test_question_data():
    return {"question_number": 1, "answer_value": 2}
