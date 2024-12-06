import pytest
from typing import AsyncGenerator, Generator
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from app.core.database import Base, get_db
from app.core.config import Settings, get_settings
from app.main import app


class TestSettings(Settings):
    # Override database settings for testing
    @property
    def ASYNC_DATABASE_URL(self) -> str:
        return "sqlite+aiosqlite:///:memory:"


# Override settings for testing
def get_test_settings() -> Settings:
    return TestSettings()


app.dependency_overrides[get_settings] = get_test_settings

engine = create_async_engine(
    get_test_settings().ASYNC_DATABASE_URL,
    poolclass=NullPool,
    connect_args={"check_same_thread": False},  # Needed for SQLite
)

TestingSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture
async def db() -> AsyncGenerator:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with TestingSessionLocal() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
def client(db: AsyncSession) -> Generator:
    async def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def test_sensor_data():
    return {"temperatura": 36.5, "ritmo_cardiaco": 85}


@pytest.fixture
def test_question_data():
    return {"question_number": 1, "answer_value": 2}
