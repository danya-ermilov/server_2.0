from typing import AsyncGenerator
from urllib.parse import quote_plus

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

from app.config import DB_CONFIG

encoded_password = quote_plus(DB_CONFIG.password)


DATABASE_URL = f"postgresql+asyncpg://{DB_CONFIG.user}:{encoded_password}@{DB_CONFIG.host}/{DB_CONFIG.database}"

engine = create_async_engine(DATABASE_URL, echo=True)

async_session = async_sessionmaker(engine, expire_on_commit=False)

Base = declarative_base()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
