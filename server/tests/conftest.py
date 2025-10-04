import pytest
import pytest_asyncio
import asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncConnection,
    AsyncTransaction,
)
from app.main import app

from urllib.parse import quote_plus
from typing import AsyncGenerator


from app.config import DB_CONFIG

from app.db.database import get_db as real_get_db

encoded_password = quote_plus(DB_CONFIG.password)


DATABASE_URL = f"postgresql+asyncpg://{DB_CONFIG.user}:{encoded_password}@{DB_CONFIG.host}/{DB_CONFIG.database_test}"

engine = create_async_engine(
    url=DATABASE_URL,
    echo=True,
)


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session")
async def connection(anyio_backend) -> AsyncGenerator[AsyncConnection, None]:
    async with engine.connect() as connection:
        yield connection


@pytest.fixture()
async def transaction(
    connection: AsyncConnection,
) -> AsyncGenerator[AsyncTransaction, None]:
    async with connection.begin() as transaction:
        yield transaction


@pytest_asyncio.fixture()
async def async_client():
    lock = asyncio.Lock()

    async def override_get_db():
        async with lock:
            async for s in real_get_db():
                yield s

    app.dependency_overrides[real_get_db] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test", follow_redirects=True
    ) as client:
        yield client

    app.dependency_overrides.pop(real_get_db, None)
