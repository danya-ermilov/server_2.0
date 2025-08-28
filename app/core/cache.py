from app.services.redis_cart import RedisCartCache

cart_cache: RedisCartCache | None = None

async def init_cache():
    global cart_cache
    cart_cache = await RedisCartCache.create()
    return cart_cache

def get_cache() -> RedisCartCache:
    if cart_cache is None:
        raise RuntimeError("Cart cache is not initialized yet")
    return cart_cache