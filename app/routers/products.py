from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user
from app.crud import products as crud_product
from app.db.database import get_db
from app.models.user import User
from app.schemas.products import ProductCreate, ProductOut, ProductUpdate

router = APIRouter(prefix="/products", tags=["Products"])


@router.post("/", response_model=ProductOut)
async def create_product(
    product_in: ProductCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    res = await crud_product.create_product(db, product_in, current_user.id)
    if not res:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="tag not found",
        )
    return res


@router.get("/my_products", response_model=List[ProductOut])
async def get_my_products(
    db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)
):
    return await crud_product.get_products_by_user(db, current_user.id)


@router.get("/", response_model=List[ProductOut])
async def list_all_products(
    tag: str = Query(None, enum=["skill_mind", "skill_sport", "skill_social", "skill_game"]),
    db: AsyncSession = Depends(get_db),
    sort_by: str = Query("life_time", enum=["life_time", "total_xp"])
):
    return await crud_product.get_all_products(db, tag, sort_by)


@router.get("/search", response_model=list[ProductOut])
async def search_products(
    q: str = Query(..., min_length=2, description="Search by product name/description"),
    db: AsyncSession = Depends(get_db),
):
    return await crud_product.search_products(db, q)


@router.get("/{product_id}", response_model=ProductOut)
async def get_product(
    product_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    product = await crud_product.get_product(db, product_id)
    if product.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="is not your product"
        )
    return product


@router.put("/{product_id}", response_model=ProductOut)
async def update_product(
    product_id: int,
    product_in: ProductUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    product = await crud_product.update_product(
        db, product_id, product_in, current_user
    )
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found or not yours",
        )
    return product


@router.delete("/{product_id}")
async def delete_product(
    product_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    deleted = await crud_product.delete_product(db, product_id, current_user)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found or not yours",
        )
    return {"message": f"Product-{product_id} deleted successfully"}


@router.get("/users/{product_id}")
async def get_users(
    product_id: int,
    db: AsyncSession = Depends(get_db),
):
    product = await crud_product.get_users_by_product(db, product_id)
    return product
