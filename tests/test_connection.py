import pytest
import asyncpg
from app.config import DB_CONFIG


@pytest.mark.asyncio
async def test_db_connection():
    conn = await asyncpg.connect(
        user=DB_CONFIG.user,
        password=DB_CONFIG.password,
        database=DB_CONFIG.database,
        host=DB_CONFIG.host,
        port=DB_CONFIG.port,
    )
    assert conn is not None
    await conn.close()
