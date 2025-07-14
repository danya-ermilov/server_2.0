from pydantic import BaseModel


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    disabled: bool = False

    class Config:
        from_attributes = True


class UserInDB(User):
    password_hash: str

    class Config:
        from_attributes = True


class TokenData(BaseModel):
    username: str | None = None
