from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.crud import comments as crud_comment
from app.db.redis import get_redis
from redis.asyncio import Redis
import json
from app.auth.dependencies import get_current_active_user
from app.schemas.users import User

router = APIRouter(prefix="/comments", tags=["Comments"])


@router.post("/products/{product_id}/comments")
async def create_comment(
    product_id: int,
    text: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    comment = await crud_comment.add_comment(db, product_id, current_user.id, text)
    redis: Redis = await get_redis()
    payload = {
        "id": comment.id,
        "product_id": product_id,
        "author": current_user.username,
        "text": text,
        "created_at": comment.created_at.isoformat(),
    }
    await redis.publish("comments_channel", json.dumps(payload))

    return payload


@router.get("/products/{product_id}/comments")
async def get_comments(product_id: int, db: AsyncSession = Depends(get_db)):
    return await crud_comment.get_comments(db, product_id)
