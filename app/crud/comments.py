from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.comment import Comment


async def add_comment(
    db: AsyncSession, product_id: int, user_id: int, text: str
) -> Comment:
    comment = Comment(product_id=product_id, author_id=user_id, text=text)
    db.add(comment)
    await db.commit()
    await db.refresh(comment)
    return comment


async def get_comments(db: AsyncSession, product_id: int):
    result = await db.execute(
        select(Comment)
        .where(Comment.product_id == product_id)
        .order_by(Comment.created_at.desc())
    )
    return result.scalars().all()
