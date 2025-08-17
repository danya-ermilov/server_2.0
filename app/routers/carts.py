from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.crud import carts, products
from app.services.redis_cart import cart_cache
from app.schemas.users import User
from app.routers.users import get_current_user



router = APIRouter(prefix="/cart", tags=["Cart"])

@router.on_event("startup")
async def startup():
    await cart_cache.connect()

@router.get("/")
async def get_cart(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    user_id = current_user.id
    cached_cart = await cart_cache.get_cached_cart(user_id)
    if cached_cart:
        return {"cart": cached_cart, "cached": True}

    items = await carts.get_cart_items(db, user_id)
    cart_data = [
        {
            "product_id": i.product_id,
            "name": i.product.name,
        } for i in items
    ]

    await cart_cache.set_cached_cart(user_id, cart_data)
    return {"cart": cart_data, "cached": False}

@router.post("/add")
async def add_to_cart(
    item_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    user_id = current_user.id
    product = await products.get_product(db, item_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    await carts.add_cart_item(db, user_id, item_id)
    await cart_cache.clear_cache(user_id)
    return {"status": "added"}

@router.delete("/")
async def clear_cart(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    user_id = current_user.id
    await carts.clear_cart_items(db, user_id)
    await cart_cache.clear_cache(user_id)
    return {"status": "cleared"}

@router.delete("/delete")
async def delete_from_cart(
    item_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    user_id = current_user.id
    product = await products.get_product(db, item_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    await carts.delete_cart_item(db, user_id, item_id)
    await cart_cache.clear_cache(user_id)
    return {"status": "deleted"}