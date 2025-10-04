from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    tag_name: str
    xp: int
    life_time: datetime
    min_xp_to_enter: Optional[int] = 0
    type_min_xp_to_enter: Optional[str] = "total_xp"


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    tag_name: Optional[str] = None
    xp: Optional[int] = None
    life_time: Optional[datetime] = None
    min_xp_to_enter: Optional[datetime] = None
    type_min_xp_to_enter: Optional[str] = None


class ProductOut(ProductBase):
    id: int
    owner_id: int
    cart_count: int

    class Config:
        orm_mode = True


# ---------- Cart ----------
class CartItemOut(BaseModel):
    id: int
    product: ProductOut

    class Config:
        orm_mode = True
