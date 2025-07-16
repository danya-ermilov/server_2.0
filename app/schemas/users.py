from pydantic import BaseModel
from typing import Optional


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    disabled: bool = False
    role: str = 'user'

    class Config:
        from_attributes = True


class UserInDB(User):
    password_hash: str

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    username: Optional[str]
    password: Optional[str]
    role: Optional[str]
    disabled: bool = False

    class Config:
        from_attributes = True


class TokenData(BaseModel):
    username: str | None = None
