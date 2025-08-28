from fastapi import FastAPI
import asyncio
from app.routers import admins, carts, products, users, comments, comments_ws
from app.db.redis import init_redis
from fastapi.staticfiles import StaticFiles
from app.core.cache import init_cache

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    await init_redis()
    await init_cache()
    from app.routers.comments_ws import redis_listener
    asyncio.create_task(redis_listener())


app.mount("/static", StaticFiles(directory="static"), name="static")


app.include_router(users.router)
app.include_router(products.router)
app.include_router(carts.router)
app.include_router(admins.router)
app.include_router(comments.router)
app.include_router(comments_ws.router)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
