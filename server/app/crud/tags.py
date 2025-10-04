from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.tag import Tag


async def add_tag(db: AsyncSession, name: str) -> Tag:
    tag = Tag(name=name)
    db.add(tag)
    await db.commit()
    await db.refresh(tag)
    return tag


async def get_tags(db: AsyncSession):
    result = await db.execute(select(Tag.name))
    return result.scalars().all()
