from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import tags as crud_tag
from app.db.database import get_db


router = APIRouter(prefix="/tags", tags=["Tags"])


@router.get("/get")
async def get_tags(db: AsyncSession = Depends(get_db)):
    """
    input: None
    do: get tags
    output: tags
    """
    return await crud_tag.get_tags(db)
