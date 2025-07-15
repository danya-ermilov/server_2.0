import asyncpg

from typing import Annotated, AsyncGenerator
from fastapi import Header, HTTPException

from app.config import DB_CONFIG


async def get_token_header(x_token: Annotated[str, Header()]):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def get_db() -> AsyncGenerator[asyncpg.Connection, None]:
    conn = await asyncpg.connect(**DB_CONFIG)
    try:
        yield conn
    finally:
        await conn.close()
