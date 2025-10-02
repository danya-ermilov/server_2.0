from fastapi import HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.cache import get_cache
from app.models.product import Product
from app.schemas.products import ProductCreate, ProductUpdate
from app.crud import tags as crud_tag
from app.models.user import User
from typing import Optional, List


async def create_product(db: AsyncSession, product_in: ProductCreate, user_id: int):
    available_tags = await crud_tag.get_tags(db)

    if product_in.tag_name not in available_tags:
        return None

    product = Product(**product_in.model_dump(), owner_id=user_id)
    db.add(product)
    await db.commit()
    await db.refresh(product)
    return product


async def get_all_products(db: AsyncSession, tag: Optional[List[str]]):
    query = select(Product)

    if tag:
        query = query.where(Product.tag_name.in_(tag))

    result = await db.execute(query)
    return result.scalars().all()


async def get_product(db: AsyncSession, product_id: int) -> Product | None:
    result = await db.execute(select(Product).where(Product.id == product_id))
    result = result.scalar_one_or_none()

    if result:
        count = await get_cache().get_cart_count(product_id)
        if not count:
            count = result.cart_count
            await get_cache().set_cart_count(product_id, count)

        result.cart_count = count
    else:
        raise HTTPException(status_code=404, detail="Product not found")
    return result


async def get_products_by_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(Product).where(Product.owner_id == user_id))
    return result.scalars().all()


async def update_product(
    db: AsyncSession, product_id: int, product_in: ProductUpdate, user: User
):
    product = await get_product(db, product_id)
    if not product:
        return None

    if product.owner_id != user.id and user.role != "admin":
        return None

    for field, value in product_in.model_dump(exclude_unset=True).items():
        setattr(product, field, value)
    await db.commit()
    await db.refresh(product)
    return product


async def delete_product(db: AsyncSession, product_id: int, user: User):
    product = await get_product(db, product_id)
    if not product:
        return False

    if product.owner_id != user.id and user.role != "admin":
        return False

    await db.delete(product)
    await db.commit()
    return True


async def search_products(db: AsyncSession, query: str):
    stmt = select(Product).where(
        Product.search_vector.op("@@")(func.plainto_tsquery("simple", query))
    )
    result = await db.execute(stmt)
    return result.scalars().all()
