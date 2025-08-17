import json
import redis.asyncio as aioredis
from typing import List, Dict
from app.config import REDIS_CONFIG

class RedisCartCache:
    def __init__(self):
        self.redis = None

    async def connect(self):
        if not self.redis:
            self.redis = await aioredis.from_url(
                f"redis://{REDIS_CONFIG.redis_host}:{REDIS_CONFIG.redis_port}/{REDIS_CONFIG.redis_db}",
                decode_responses=True,
            )

    async def get_cached_cart(self, user_id: int) -> List[Dict] | None:
        data = await self.redis.get(f"cart:{user_id}")
        return json.loads(data) if data else None

    async def set_cached_cart(self, user_id: int, cart: List[Dict]):
        await self.redis.set(f"cart:{user_id}", json.dumps(cart), ex=300)  # 5 минут TTL

    async def clear_cache(self, user_id: int):
        await self.redis.delete(f"cart:{user_id}")

cart_cache = RedisCartCache()
