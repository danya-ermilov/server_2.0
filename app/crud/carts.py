from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.cart import CartItem


async def get_cart_items(db: AsyncSession, user_id: int):
    result = await db.execute(select(CartItem).filter(CartItem.user_id == user_id))
    return result.scalars().all()


async def add_cart_item(db: AsyncSession, user_id: int, product_id: int):
    item = CartItem(user_id=user_id, product_id=product_id)
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return item


async def delete_cart_item(db: AsyncSession, user_id: int, product_id: int):
    result = await db.execute(
        select(CartItem).where(
            CartItem.user_id == user_id, CartItem.product_id == product_id
        )
    )
    item = result.scalar_one_or_none()
    if not item:
        return None
    await db.delete(item)
    await db.commit()
    return item


async def clear_cart_items(db: AsyncSession, user_id: int):
    await db.execute(CartItem.__table__.delete().where(CartItem.user_id == user_id))
    await db.commit()
