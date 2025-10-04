from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel


# -------------------------
# Агрегаты XP пользователя
# -------------------------
class UserStatBase(BaseModel):
    total_xp: int = 0
    skill_mind: int = 0
    skill_social: int = 0
    skill_sport: int = 0
    skill_game: int = 0


class UserStat(UserStatBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True


# -------------------------
# История начислений XP
# -------------------------
class XpHistoryBase(BaseModel):
    category: str
    points: int
    product_id: int


class XpHistoryCreate(XpHistoryBase):
    user_id: int


class XpHistory(XpHistoryBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# -------------------------
# Пользователь
# -------------------------
class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    disabled: bool = False
    role: str = "user"
    stats: Optional[UserStat] = None
    xp_records: Optional[List[XpHistory]] = []

    class Config:
        from_attributes = True


class UserInDB(User):
    password_hash: str

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    role: Optional[str] = None
    disabled: bool = False

    class Config:
        from_attributes = True


# -------------------------
# Токен
# -------------------------
class TokenData(BaseModel):
    username: Optional[str] = None
