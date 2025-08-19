from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.product import Product
from app.schemas.products import ProductCreate, ProductUpdate

from app.models.user import User


async def create_product(db: AsyncSession, product_in: ProductCreate, user_id: int):
    product = Product(**product_in.model_dump(), owner_id=user_id)
    db.add(product)
    await db.commit()
    await db.refresh(product)
    return product


async def get_all_products(db: AsyncSession):
    result = await db.execute(select(Product))
    return result.scalars().all()


async def get_product(db: AsyncSession, product_id: int):
    result = await db.execute(select(Product).where(Product.id == product_id))
    return result.scalar_one_or_none()


async def get_products_by_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(Product).where(Product.owner_id == user_id))
    return result.scalars().all()


async def update_product(
    db: AsyncSession, product_id: int, product_in: ProductUpdate, user: User
):
    product = await get_product(db, product_id)
    if not product:
        return None

    if product.owner_id != user.id or user.role != "admin":
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

    if product.owner_id != user.id or user.role != "admin":
        return False

    await db.delete(product)
    await db.commit()
    return True
