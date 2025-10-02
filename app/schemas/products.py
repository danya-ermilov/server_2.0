from typing import Optional

from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    tag_name: str
    xp: int


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    tag_name: Optional[str] = None
    xp: Optional[int] = None


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
