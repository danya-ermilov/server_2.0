from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user
from app.crud import carts as crud_cart, products as crud_product
from app.db.database import get_db
from app.schemas.users import User
from app.core.cache import get_cache

router = APIRouter(prefix="/cart", tags=["Cart"])


@router.get("/")
async def get_cart(
    current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    """
    input: None
    do: get cart
    output: {"cart": cart_data, "cached": False}
    """
    user_id = current_user.id
    cached_cart = await get_cache().get_cached_cart(user_id)
    if cached_cart:
        return {"cart": cached_cart, "cached": True}

    items = await crud_cart.get_cart_items(db, user_id)
    cart_data = [
        {
            "name": i.product.name,
            "description": i.product.description,
        }
        for i in items
    ]

    await get_cache().set_cached_cart(user_id, cart_data)
    return {"cart": cart_data, "cached": False}


@router.post("/add")
async def add_to_cart(
    item_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    input: item_id : int
    do: add event to cart
    output: {"status": "added"}
    """
    user_id = current_user.id
    product = await crud_product.get_product(db, item_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    cart = (i.product_id for i in await crud_cart.get_cart_items(db, user_id))
    if item_id not in cart:
        await crud_cart.add_cart_item(db, user_id, item_id)
        await get_cache().clear_cache(user_id)
        return {"status": "added"}
    else:
        return "already in cart"


@router.delete("/")
async def clear_cart(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    input: None
    do: delete all from cart
    output: {"status": "cleared"}
    """
    user_id = current_user.id
    await crud_cart.clear_cart_items(db, user_id)
    await get_cache().clear_cache(user_id)
    return {"status": "cleared"}


@router.delete("/delete")
async def delete_from_cart(
    item_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    input: item_id : int
    do: delete event from cart
    output: {"status": "deleted"}
    """
    user_id = current_user.id
    product = await crud_product.get_product(db, item_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    await crud_cart.delete_cart_item(db, user_id, item_id)
    await get_cache().clear_cache(user_id)
    return {"status": "deleted"}
