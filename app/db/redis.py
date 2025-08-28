import redis.asyncio as aioredis
from app.config import REDIS_CONFIG


REDIS_URL = f"redis://{REDIS_CONFIG.redis_host}:{REDIS_CONFIG.redis_port}/{REDIS_CONFIG.redis_db}"

_redis: aioredis.Redis | None = None


async def init_redis():
    global _redis
    if not _redis:
        _redis = await aioredis.from_url(REDIS_URL, decode_responses=True)
    return _redis


async def get_redis():
    if not _redis:
        raise RuntimeError("Redis not initialized")
    return _redis


async def close_redis():
    global _redis
    if _redis:
        await _redis.close()
        _redis = None
