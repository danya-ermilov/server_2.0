from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.db.redis import get_redis
import json
from redis.asyncio import Redis

router = APIRouter(prefix="/comments-ws", tags=["Comments-ws"])
CHANNEL = "comments_channel"

connections: dict[int, set[WebSocket]] = {}


@router.websocket("/ws/comments/{product_id}")
async def comments_ws(websocket: WebSocket, product_id: int):
    """
    input: websocket : WebSocket, product_id : int
    do: get ws chat
    output: None
    """
    await websocket.accept()
    connections.setdefault(product_id, set()).add(websocket)

    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        connections[product_id].remove(websocket)
        if not connections[product_id]:
            del connections[product_id]


async def redis_listener():
    redis: Redis = await get_redis()
    pubsub = redis.pubsub()
    await pubsub.subscribe(CHANNEL)

    async for message in pubsub.listen():
        if message["type"] == "message":
            comment = json.loads(message["data"])
            product_id = comment["product_id"]

            if product_id in connections:
                dead = []
                for ws in connections[product_id]:
                    try:
                        await ws.send_json(comment)
                    except Exception:
                        dead.append(ws)
                for ws in dead:
                    connections[product_id].remove(ws)
