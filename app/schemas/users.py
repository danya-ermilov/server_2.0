from typing import Optional

from pydantic import BaseModel


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
    username: Optional[str]= None
    password: Optional[str] = None
    role: Optional[str]= None
    disabled: bool = False

    class Config:
        from_attributes = True


class TokenData(BaseModel):
    username: str | None = None
