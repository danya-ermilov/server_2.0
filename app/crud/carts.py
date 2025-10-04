from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.cart import CartItem
from app.crud import products as crud_product
from app.crud import users as crud_user
from app.core.cache import get_cache
from fastapi import HTTPException


async def get_cart_items(db: AsyncSession, user_id: int):
    result = await db.execute(select(CartItem).filter(CartItem.user_id == user_id))
    return result.scalars().all()


async def add_cart_item(db: AsyncSession, user_id: int, product_id: int):
    item = CartItem(user_id=user_id, product_id=product_id)
    user = await crud_user.get_user(db, user_id)
    user = await crud_user.get_user_with_xp(db, user.username)
    product = await crud_product.get_product(db, product_id)

    user_xp = user[0].get(product.type_min_xp_to_enter)
    if user_xp is None:
        for stat in user:
            if stat.get('product') == product.type_min_xp_to_enter:
                user_xp = stat['total_points']
                break

    if user_xp is None or user_xp < product.min_xp_to_enter:
        raise HTTPException(
            status_code=400,
            detail=f"Недостаточно опыта для добавления продукта в корзину. Требуется {product.min_xp_to_enter}, у вас {user_xp}"
        )
    product.cart_count += 1

    db.add(item)
    await get_cache().incr_cart_count(product_id)

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

    product = await crud_product.get_product(db, product_id)
    product.cart_count -= 1

    await get_cache().decr_cart_count(product_id)

    await db.delete(item)
    await db.commit()
    return item


async def clear_cart_items(db: AsyncSession, user_id: int):
    all_items_in_cart = await get_cart_items(db, user_id)

    for item in all_items_in_cart:
        item.product.cart_count -= 1
        await get_cache().decr_cart_count(item.product_id)

    await db.execute(CartItem.__table__.delete().where(CartItem.user_id == user_id))
    await db.commit()
