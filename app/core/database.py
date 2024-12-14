from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import NullPool

from app.core.config import get_settings

# Create Base class for models
Base = declarative_base()


# Create async engine and session factory
def get_engine():
    settings = get_settings()
    return create_async_engine(
        settings.ASYNC_DATABASE_URL,
        echo=True,
        poolclass=NullPool,
    )


def get_sessionmaker():
    return sessionmaker(
        get_engine(),
        class_=AsyncSession,
        expire_on_commit=False,
    )


# Create session dependency
async def get_db():
    async_session = get_sessionmaker()
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()
