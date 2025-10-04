import json
from typing import Dict, List

import redis.asyncio as aioredis
from app.core.config import REDIS_URL

from app.db.redis import get_redis


class RedisCartCache:
    def __init__(self, redis):
        self.redis = redis

    @classmethod
    async def create(cls):
        redis = await get_redis()
        return cls(redis)

    async def connect(self):
        if not self.redis:
            self.redis = await aioredis.from_url(
                REDIS_URL,
                decode_responses=True,
            )

    async def get_cached_cart(self, user_id: int) -> List[Dict] | None:
        data = await self.redis.get(f"cart:{user_id}")
        return json.loads(data) if data else None

    async def set_cached_cart(self, user_id: int, cart: List[Dict]):
        await self.redis.set(f"cart:{user_id}", json.dumps(cart), ex=300)

    async def clear_cache(self, user_id: int):
        await self.redis.delete(f"cart:{user_id}")

    async def incr_cart_count(self, product_id: int):
        await self.redis.incr(f"cart_count:{product_id}")

    async def decr_cart_count(self, product_id: int):
        await self.redis.decr(f"cart_count:{product_id}")

    async def get_cart_count(self, product_id: int, default: int = 0) -> int:
        value = await self.redis.get(f"cart_count:{product_id}")
        if value is None:
            return default
        return int(value)

    async def set_cart_count(self, product_id: int, count: int):
        await self.redis.set(f"cart_count:{product_id}", count)
